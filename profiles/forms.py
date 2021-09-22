from django import forms


class RegisterForm(forms.Form):
    login = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField()
    password_repeat = forms.CharField()


class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField()


