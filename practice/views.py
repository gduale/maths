import uuid
from django.contrib import messages
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import AVATARS, Attempt, Profile
from .exercises import OPERATIONS, generate_questions

def owner(request):
    if "owner" not in request.session:
        request.session["owner"] = uuid.uuid4().hex
    return request.session["owner"]

def home(request):
    profiles = Profile.objects.filter(owner=owner(request))
    return render(request, "practice/home.html", {"profiles": profiles, "avatars": AVATARS, "operations": OPERATIONS.items(), "selected": request.session.get("profile")})

@require_POST
def create_profile(request):
    name = request.POST.get("name", "").strip()
    avatar = request.POST.get("avatar")
    if name and len(name) <= 30 and avatar in dict(AVATARS):
        profile = Profile.objects.create(owner=owner(request), first_name=name, avatar=avatar)
        request.session["profile"] = profile.pk
    return redirect("home")

@require_POST
def select_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk, owner=owner(request))
    request.session["profile"] = profile.pk
    return redirect("home")

def tables(request, operation):
    if operation not in OPERATIONS:
        raise Http404
    return render(request, "practice/tables.html", {"operation": operation, "details": OPERATIONS[operation], "tables": range(2, 10)})

@require_POST
def start(request, operation, table):
    if operation not in OPERATIONS or table not in range(2, 10):
        raise Http404
    profile = Profile.objects.filter(pk=request.session.get("profile"), owner=owner(request)).first()
    if not profile:
        messages.info(request, "Crée ou choisis ton profil pour commencer ta mission !")
        return redirect("home")
    attempt = Attempt.objects.create(profile=profile, operation=operation, table=table, questions=generate_questions(operation, table))
    return redirect("exercise", pk=attempt.pk)

def exercise(request, pk):
    with transaction.atomic():
        attempt = get_object_or_404(Attempt.objects.select_for_update(), pk=pk, profile__owner=owner(request))
        count = len(attempt.answers)
        if request.method == "POST" and not attempt.finished_at:
            raw = request.POST.get("answer", "")
            if request.POST.get("index") == str(count) and raw.isascii() and raw.isdigit() and len(raw) <= 3:
                value = int(raw)
                correct = value == attempt.questions[count]["answer"]
                attempt.answers.append({"value": value, "correct": correct})
                attempt.score += int(correct)
                if len(attempt.answers) == 10:
                    attempt.finished_at = timezone.now()
                    attempt.duration_seconds = round((attempt.finished_at - attempt.started_at).total_seconds())
                attempt.save()
                return redirect(f"/exercice/{pk}/?feedback=1")
        feedback = request.GET.get("feedback") == "1" and bool(attempt.answers)
        if attempt.finished_at and not feedback:
            return render(request, "practice/result.html", {"attempt": attempt})
        index = len(attempt.answers) - 1 if feedback else len(attempt.answers)
        question = attempt.questions[index]
        return render(request, "practice/exercise.html", {"attempt": attempt, "question": question, "index": index, "number": index + 1, "progress": (index + 1) * 10, "details": OPERATIONS[attempt.operation], "feedback": feedback, "last_answer": attempt.answers[-1] if feedback else None, "digits": "1234567890"})

def history(request):
    attempts = Attempt.objects.filter(profile__owner=owner(request), finished_at__isnull=False).select_related("profile").order_by("-finished_at")[:100]
    return render(request, "practice/history.html", {"attempts": attempts})
