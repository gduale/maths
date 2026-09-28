from django.db import migrations


def initialize_counter(apps, schema_editor):
    database = schema_editor.connection.alias
    Attempt = apps.get_model("practice", "Attempt")
    UsageCounter = apps.get_model("practice", "UsageCounter")
    answered_questions = 0
    completed_series = 0
    for attempt in Attempt.objects.using(database).only("answers", "finished_at").iterator():
        answered_questions += len(attempt.answers)
        completed_series += int(attempt.finished_at is not None)
    UsageCounter.objects.using(database).update_or_create(
        pk=1,
        defaults={
            "answered_questions": answered_questions,
            "completed_series": completed_series,
        },
    )


class Migration(migrations.Migration):
    dependencies = [("practice", "0002_usagecounter")]

    operations = [migrations.RunPython(initialize_counter, migrations.RunPython.noop)]
