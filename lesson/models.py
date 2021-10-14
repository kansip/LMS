from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL
from course.models import Course
# Create your models here.

class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    #blocks = models.ManyToManyField(TaskGroup)
    teacher = models.OneToOneField(User, on_delete=SET_NULL,null=True)
    name = models.CharField(max_length=30)
    date = models.DateTimeField()
    open = models.BooleanField(default=False)