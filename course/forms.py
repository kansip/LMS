""" Формы, каким либо способом связанные с курсами """
from django import forms
from django.contrib.auth.models import Group

class CreateCourseForm(forms.Form):
    """ Форма создания нового курса"""
    name = forms.CharField(required=False)
    description = forms.CharField(required=False)
    image = forms.ImageField(required=False)


class SettingsInfoCourseForm(forms.Form):
    """ Форма изменения основоной информации курса"""
    name = forms.CharField(required=False)
    description = forms.CharField(required=False)
    image = forms.ImageField(required=False)
    #teachers = forms.ChoiceField(choices = [(user.id, user.username) for user in Group.objects.get(name="teachers").user_set.all()],required=False)
    open = forms.BooleanField(required=False)

class SettingsStudentListCourseForm(forms.Form):
    """ Форма добавление нового пользователя курса"""
    id = forms.IntegerField()