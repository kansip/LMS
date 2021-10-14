from unittest import signals
from course.forms import CreateCourseForm, SettingsInfoCourseForm
from django.http.response import Http404
from course.models import Course
from lesson.models import Lesson
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect, render
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from LMS_settings.menu import get_context_menu, HOME_PAGE_NAME,COURSE_CREATE_NAME,COURSE_STUDY_NAME,COURSE_TEACHING_NAME
from django.core.files.storage import FileSystemStorage
from course.utils import group_course_name
# Create your views here.

@login_required
def course_view(request, course_id):
    """Просмотр содержания курса"""
    context = {'menu': get_context_menu(request, COURSE_STUDY_NAME)} #заменить
    try:
        course=Course.objects.get(id=course_id)
        context['course']=course
        context['lessons']=Lesson.objects.filter(course_id=course_id)
        name_group=group_course_name(course_id)
        if request.user.groups.filter(name=name_group).exists():
            return render(request, 'course.html', context)
        elif request.user == course.teacher:
            return render(request, 'course.html', context)
        else:
            raise Http404("Вы не подключены к курсу")
    except Course.DoesNotExist: #Ответ на не найденный курс
        raise Http404("There is no course with this id")
    except Group.DoesNotExist: #Ответ на не существующую группу
        raise Http404("You don't belong to this group")

@login_required
def course_study_list(request):
    """Список курс, на которых обучается пользователь"""
    context = {'menu': get_context_menu(request, COURSE_STUDY_NAME)} 
    groups_users = request.user.groups.all()
    courses=[]
    for group in groups_users:
        try:
            course=Course.objects.get(students=group)
        except:
            continue
        if course.open:
            courses.append(course)
    context["courses"]=courses
    return render(request, 'course_study.html', context)

@staff_member_required
def course_create(request):
    """Создание курса"""
    context = {'menu': get_context_menu(request, COURSE_CREATE_NAME)} 
    if request.method == 'POST':
        create_course_form = CreateCourseForm(request.POST)
        #print(create_course_form.is_valid())
        if create_course_form.is_valid():
            # получение данных из формы
            name_date = create_course_form.cleaned_data['name']
            description_date = create_course_form.cleaned_data['description']
            image_date = request.FILES['image']

            # сохраняем картинку на файловой системе
            fs = FileSystemStorage()
            filename = fs.save(image_date.name, image_date)

            #создаем курс
            course = Course.objects.create(name=name_date,description=description_date, image=image_date,teacher=request.user)
            
            name_group=group_course_name(course.id)
            group=Group.objects.create(name=name_group)
            course.students = group
            course.save()
            return redirect("/course/"+str(course.id))
    return render(request, 'course_create.html', context)

@staff_member_required
def course_teaching_list(request):
    """Список курсов, на которых преподает аккаунт"""
    context = {'menu': get_context_menu(request, COURSE_TEACHING_NAME)}
    context["courses"]=Course.objects.filter(teacher=request.user)
    return render(request, 'course_teaching.html', context)

@staff_member_required
def course_settings(request, course_id):
    context = {'menu': get_context_menu(request, COURSE_TEACHING_NAME)}
    try:
        course = Course.objects.get(id=course_id)
        context["course"] = course
        context["teachers"] = Group.objects.get(name="teachers").user_set.all()
        context["students"] = Course.objects.get(id=course_id).students.user_set.all()
        context['lessons'] = Lesson.objects.filter(course_id=course_id)
    except:
        raise Http404("Такого курса не существует")
    if request.method == 'POST':
        if 'main_info' in request.POST:
            settings_info_course = SettingsInfoCourseForm(request.POST)
            if settings_info_course.is_valid():
                name = settings_info_course.cleaned_data['name']
                description = settings_info_course.cleaned_data['description']
                open = settings_info_course.cleaned_data['open']
                course.name = name
                course.description = description
                if 'open' in request.POST:
                    course.open = True
                else:
                    course.open = False
                if  'image' in request.FILES:
                    # сохраняем на картинку файловой системе
                    file = request.FILES['image']
                    fs = FileSystemStorage()
                    filename = fs.save(file.name, file)
                    course.image = file
                course.save()
                
        elif "add_user_to_course" in request.POST:
            pass
    return render(request, 'course_settings.html', context)

@staff_member_required
def course_delete(request, course_id):
    """Удаление курса с переданным id"""
    context = {'menu': get_context_menu(request, COURSE_TEACHING_NAME)}
    try:
        Group.objects.filter(name=group_course_name(course_id)).delete()
        Course.objects.filter(id=course_id).delete()
    except:
        raise Http404("Косяк при удаление курса")
    return redirect('/')

@staff_member_required
def course_settings_info(request, course_id):
    pass