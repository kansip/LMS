""" Формы, каким либо способом связанные с пользователем """
from django import forms

class RegisterForm(forms.Form):
    """ Форма регистрации нового пользователя """
    login = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField()
    password_repeat = forms.CharField()

class LoginForm(forms.Form):
    """ Форма авторизации нового пользователя """
    login = forms.CharField()
    password = forms.CharField()
    