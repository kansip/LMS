from LMS_settings.celery import app
from lesson.models import Lesson
from django.utils import timezone
@app.task
def open_lesson(lesson_id):
    #print("HI")
    lesson = Lesson.objects.get(id=lesson_id)
    if lesson.date <= timezone.now():
        lesson.open = True
        lesson.save()
        return True
    else:
        return False