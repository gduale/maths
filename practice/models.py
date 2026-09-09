from django.db import models

AVATARS = [("fox", "🦊"), ("cat", "🐱"), ("panda", "🐼"), ("frog", "🐸"), ("rabbit", "🐰"), ("lion", "🦁")]

class Profile(models.Model):
    owner = models.CharField(max_length=64, db_index=True)
    first_name = models.CharField(max_length=30)
    avatar = models.CharField(max_length=12, choices=AVATARS, default="fox")

    def __str__(self):
        return self.first_name

class Attempt(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="attempts")
    operation = models.CharField(max_length=12)
    table = models.PositiveSmallIntegerField()
    questions = models.JSONField()
    answers = models.JSONField(default=list)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    score = models.PositiveSmallIntegerField(default=0)
