from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

class TaskFiles(models.Model):
    files = models.FileField(upload_to = 'uploads/')

class Task(models.Model):
    name = models.CharField(max_length = 120)
    desc = RichTextUploadingField(blank=True, null=True)
    cost = models.IntegerField()
    files = models.ManyToManyField(TaskFiles)
    revizion_format_flag = models.BooleanField(default = 0)
    file_format_flag = models.BooleanField(default = 0)
    text_format_flag = models.BooleanField(default = 1)
    number_of_attempts = models.IntegerField(default=100)

class TaskAnswers(models.Model):
    answer = models.TextField()
    user = models.ForeignKey(User, null = True, on_delete = models.SET_NULL)
    time = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField()
    revizion = models.BooleanField(default = 0)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

class TaskTrueAnswers(models.Model):
    task_id = models.ForeignKey(Task, on_delete = models.CASCADE)
    true_flags = models.TextField()


class TaskGroup(models.Model):
    name = models.CharField(max_length = 100)
    local = models.IntegerField(default=1)
    date_open = models.DateTimeField(null=True)
    date_part_close = models.DateTimeField(null=True)
    date_close = models.DateTimeField(null=True)
    open = models.BooleanField(default=0)
    tasks = models.ManyToManyField(Task)