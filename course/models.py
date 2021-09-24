from django.db import models
from django.contrib.auth.models import User,Group
# Create your models here.


class Course(models.Model):
    teacher = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='course', blank=True)
    description = models.CharField(max_length=100)
    open = models.BooleanField(default=False)
    students = models.ForeignKey(Group,null=True,on_delete=models.SET_NULL)