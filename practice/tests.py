from datetime import timedelta
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from .exercises import OPERATIONS, generate_questions
from .models import Attempt, Profile


class ExerciseGenerationTests(TestCase):
    def test_all_tables_have_ten_distinct_valid_questions(self):
        for operation in OPERATIONS:
            for table in range(2, 10):
                for _ in range(20):
                    questions = generate_questions(operation, table)
                    self.assertEqual(len(questions), 10)
                    self.assertEqual(len({(q['left'], q['right'], q['result'], q['hole']) for q in questions}), 10)
                    for position in ('left', 'right', 'result'):
                        self.assertIn(sum(q['hole'] == position for q in questions), (3, 4))
                    for question in questions:
                        left, right, result = (question[key] for key in ('left', 'right', 'result'))
                        calculated = {'addition': lambda: left + right, 'soustraction': lambda: left - right, 'multiplication': lambda: left * right, 'division': lambda: left / right}[operation]()
                        self.assertEqual(calculated, result)
                        self.assertEqual(question['answer'], question[question['hole']])
                        self.assertGreaterEqual(question['answer'], 0)
                        self.assertEqual(result, int(result))


class JourneyTests(TestCase):
    def setUp(self):
        self.client.post(reverse('create_profile'), {'name': 'Camille', 'avatar': 'fox'})
        self.profile = Profile.objects.get()

    def start_attempt(self):
        response = self.client.post(reverse('start', args=['addition', 2]))
        self.assertEqual(response.status_code, 302)
        return Attempt.objects.latest('pk')

    def test_complete_series_saves_score_and_server_duration(self):
        attempt = self.start_attempt()
        Attempt.objects.filter(pk=attempt.pk).update(started_at=timezone.now() - timedelta(seconds=42))
        url = reverse('exercise', args=[attempt.pk])
        for index, question in enumerate(attempt.questions):
            response = self.client.post(url, {'index': index, 'answer': question['answer']}, follow=True)
            self.assertContains(response, 'Bien joué')
        attempt.refresh_from_db()
        self.assertEqual(attempt.score, 10)
        self.assertGreaterEqual(attempt.duration_seconds, 42)
        self.assertIsNotNone(attempt.finished_at)
        self.assertContains(self.client.get(url), 'Bravo Camille')
        self.assertContains(self.client.get(reverse('history')), '10 / 10')

    def test_duplicate_invalid_and_wrong_answers(self):
        attempt = self.start_attempt()
        url = reverse('exercise', args=[attempt.pk])
        self.client.post(url, {'index': 0, 'answer': '-1'})
        attempt.refresh_from_db()
        self.assertEqual(attempt.answers, [])
        response = self.client.post(url, {'index': 0, 'answer': '999'}, follow=True)
        self.assertContains(response, 'Bien essayé')
        self.client.post(url, {'index': 0, 'answer': '999'})
        attempt.refresh_from_db()
        self.assertEqual(len(attempt.answers), 1)
        self.assertEqual(attempt.score, 0)

    def test_profiles_and_attempts_are_private_to_browser(self):
        attempt = self.start_attempt()
        other = Client()
        self.assertEqual(list(other.get('/').context['profiles']), [])
        self.assertEqual(other.get(reverse('exercise', args=[attempt.pk])).status_code, 404)
        self.assertEqual(other.post(reverse('select_profile', args=[self.profile.pk])).status_code, 404)

    def test_invalid_routes_and_missing_profile(self):
        self.assertEqual(self.client.get('/tables/invalid/').status_code, 404)
        self.assertEqual(self.client.post('/demarrer/addition/12/').status_code, 404)
        self.assertRedirects(Client().post('/demarrer/addition/2/'), '/')

    def test_all_pages_render(self):
        for operation in OPERATIONS:
            self.assertEqual(self.client.get(reverse('tables', args=[operation])).status_code, 200)
        self.assertContains(self.client.get('/'), 'Camille')
        self.assertEqual(self.client.get('/historique/').status_code, 200)

    def test_missing_result_is_rendered_and_checked_for_each_operation(self):
        for operation in OPERATIONS:
            with self.subTest(operation=operation):
                questions = generate_questions(operation, 9)
                questions.sort(key=lambda question: question['hole'] != 'result')
                attempt = Attempt.objects.create(profile=self.profile, operation=operation, table=9, questions=questions)
                url = reverse('exercise', args=[attempt.pk])
                response = self.client.get(url)
                self.assertContains(response, '<span>=</span><input aria-label="Nombre manquant"')
                self.assertContains(response, 'name="answer"', count=1)
                response = self.client.post(url, {'index': 0, 'answer': questions[0]['result']}, follow=True)
                self.assertContains(response, 'Bien joué')
                attempt.refresh_from_db()
                self.assertEqual(attempt.score, 1)
