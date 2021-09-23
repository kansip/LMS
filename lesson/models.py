from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Lesson(models.Model):
    teacher = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(null=True)
    #blocks = models.ManyToManyField(TaskGroup)
    name = models.CharField(max_length=30)
    open = models.BooleanField(default=False)