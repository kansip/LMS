""" Формы, каким либо способом связанные с курсами """
from django import forms

class CreateCourseForm(forms.Form):
    """ Форма создания нового курса"""
    name = forms.CharField(required=False)
    description = forms.CharField(required=False)
    image = forms.ImageField(required=False)


class SettingsInfoCourseForm(forms.Form):
    """ Форма создания нового курса"""
    name = forms.CharField(required=False)
    description = forms.CharField(required=False)
    image = forms.ImageField(required=False)
    #teacher = forms.