from django.db import models
from django.contrib.auth.models import User


class TaskFiles(models.Model):
    files = models.FileField(upload_to = 'uploads/')


class TaskAnswers(models.Model):
    answer = models.TextField()
    user = models.ForeignKey(User, null = True, on_delete = models.SET_NULL)
    time = models.DateTimeField()
    score = models.IntegerField()
    revizion = models.BooleanField(default = 0)

class Task(models.Model):
    name = models.CharField(max_length = 120)
    desc = models.TextField()
    cost = models.IntegerField()
    category = models.CharField(max_length = 20)
    files = models.ManyToManyField(TaskFiles)
    revizion_format_flag = models.BooleanField(default = 0)


class TaskTrueAnswers(models.Model):
    task_id = models.ForeignKey(Task, on_delete = models.CASCADE)
    true_flags = models.TextField()


class TaskGroup(models.Model):
    name = models.CharField(max_length = 100)
    author = models.ForeignKey(User, null = True, on_delete = models.SET_NULL)
    local = models.IntegerField()
    data_open = models.DateTimeField()
    data_part_close = models.DateTimeField()
    data_close = models.DateTimeField()
    open = models.BooleanField()
    tasks = models.ManyToManyField(Task)