from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL
from course.models import Course
from tasks.models import TaskGroup
# Create your models here.

class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    #blocks = models.ManyToManyField(TaskGroup)
    teacher = models.ForeignKey(User, on_delete=SET_NULL,null=True)
    name = models.CharField(max_length=30)
    date = models.DateTimeField(null=True)
    open = models.BooleanField(default=False)
    blocks = models.ManyToManyField(TaskGroup)