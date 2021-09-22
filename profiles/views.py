""" Функции обработки взаимодействия с user"""
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from LMS_settings.menu import get_context_menu, REGISTER_PAGE_NAME, LOGIN_PAGE_NAME
from profiles.forms import RegisterForm, LoginForm


def index(request):
    """ Функция редиректа на главную страницу, либо же """

    if not request.user.is_authenticated:
        return redirect('/login')
    return redirect('/main')


def register_view(request):
    """ Функция регистрации нового пользователя  """

    context = {'menu': get_context_menu(request, REGISTER_PAGE_NAME)}

    if request.method == 'POST':
        errors = []

        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            login_data = register_form.cleaned_data['login']
            first_name = register_form.cleaned_data['first_name']
            last_name = register_form.cleaned_data['last_name']
            password_data = register_form.cleaned_data['password']
            password_repeat_data = register_form.cleaned_data['password_repeat']

            if len(login_data) < 3:
                errors.append('Логин должен иметь длину больше 2 символов')

            if User.objects.filter(username=login_data).exists():
                errors.append('Пользователь с таким логином уже существует')

            if len(password_data) < 4:
                errors.append('Пароль должен иметь длину больше 3 символов')

            if password_data != password_repeat_data:
                errors.append('Пароли не совпадают')

            if len(errors) == 0:
                user = User.objects.create_user(username=login_data, password=password_data,
                                                first_name=first_name,
                                                last_name=last_name)
                user.save()

                if user is not None:
                    login(request, user)
                    return redirect('/')

                return redirect('/')
        else:
            errors.append('Заполните все поля')

        context['error'] = errors[0]

    return render(request, 'register.html', context)


def login_view(request):
    """ Функция авторизации нового пользователя  """

    context = {'menu': get_context_menu(request, LOGIN_PAGE_NAME)}

    if not request.user.is_authenticated:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)

            if login_form.is_valid():
                login_data = login_form.cleaned_data['login']
                password_data = login_form.cleaned_data['password']

                print(login_data)
                print(password_data)

                user = authenticate(request, username=login_data, password=password_data)

                if user is not None:
                    login(request, user)
                    return redirect('/')

            context['error'] = 'Неверный логин или пароль'

        return render(request, 'login.html', context)
    return redirect('/')
