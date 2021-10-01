from django.db import models
from django.contrib.auth.models import User
from course.models import Course
# Create your models here.

class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    #blocks = models.ManyToManyField(TaskGroup)
    name = models.CharField(max_length=30)
    date = models.DateTimeField()
    open = models.BooleanField(default=False)