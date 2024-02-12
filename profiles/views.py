""" Функции обработки взаимодействия с user"""
from django.contrib.auth import authenticate, login, logout
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.admin.views.decorators import staff_member_required
from LMS_settings.menu import *
from profiles.forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import user_passes_test


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

                user = authenticate(request, username=login_data, password=password_data)

                if user is not None:
                    login(request, user)
                    return redirect('/')

            context['error'] = 'Неверный логин или пароль'

        return render(request, 'login.html', context)
    return redirect('/')


@login_required
def main_page_view(request):
    """ Главная страница """
    context = {'menu': get_context_menu(request, HOME_PAGE_NAME)}
    return render(request, 'index.html', context)

@login_required
def logout_view(request):
    """ Выход из аккаунта"""
    logout(request)
    return redirect('/')

@login_required
def user_page_view(request, user_id):
    """ Личный кабинет пользователя
        Видно только самому пользователю и сотрудникам
        :param user_id: - Уникальный номер получаемого пользователя
    
    """
    context = {'menu': get_context_menu(request, USER_PAGE_NAME)}
    try:
        user = User.objects.get(id=user_id)
        context["user"]=user
    except:
        raise Http404("Такого нет")
    if request.user.is_staff or request.user.id==user_id:
        return render(request, 'user.html', context)
    else:
        raise Http404("У вас нет прав")

@staff_member_required
def user_list_view(request):
    context = {'menu': get_context_menu(request, USER_LIST_NAME)}
    context["users"] = User.objects.all()
    return render(request,"user_list.html",context)


@user_passes_test(lambda u: u.is_superuser) 
def user_settings_view(request, user_id):
    context = {'menu': get_context_menu(request, USER_LIST_NAME)}
    context["groups"] = Group.objects.all()
    user=User.objects.get(id=user_id)
    context["user"] = user
    if request.method == "POST":
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        password = request.POST['password']
        if password != '':
            user.set_password(password)
        if 'ban' in request.POST:
            user.is_active = False
        else:
            user.is_active = True
        if 'teacher' in request.POST:
            user.is_staff = True
            group = Group.objects.get(name='teachers')
            group.user_set.add(user)
        else:
            user.is_staff = False
            group = Group.objects.get(name='teachers')
            group.user_set.remove(user)
            
        if 'admin' in request.POST:
            user.is_superuser = True
            group = Group.objects.get(name='admins')
            group.user_set.add(user)
        else:
            user.is_superuser = False
            group = Group.objects.get(name='admins')
            group.user_set.remove(user)
        user.save()
    return render(request,"user_settings.html",context)