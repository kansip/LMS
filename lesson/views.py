from ctypes import resize
import re
from typing import TYPE_CHECKING
from tasks.models import TaskGroup
from django.contrib.auth.models import Group, User
from lesson.models import Lesson
from course.models import Course
from lesson.forms import AddBlockForm
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render
from LMS_settings.menu import get_context_menu, HOME_PAGE_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.

@login_required
def lesson_view(request, course_id, lesson_id):
    """ Просмотр определенного занятия"""
    context = {'menu': get_context_menu(request, HOME_PAGE_NAME)} #заменить3
    try:
        context['lesson']=Lesson.objects.get(id=lesson_id)
        context['course']=Course.objects.get(id=course_id)
        context['blocks']=Lesson.objects.get(id=lesson_id).blocks.all()
    except:
        raise Http404("Такого занятия нет")
    return render(request,'lesson.html',context)

@staff_member_required
def settings(request, course_id, lesson_id):
    """ Настроек конкретного занятия <lesson_id> """
    context = {'menu': get_context_menu(request, HOME_PAGE_NAME)} #заменить
    try:
        lesson=Lesson.objects.get(id=lesson_id)
        context['lesson']=lesson
        context["teachers"] = Group.objects.get(name="teachers").user_set.all()
        context['course']=Course.objects.get(id=course_id)
        context['blocks']=Lesson.objects.get(id=lesson_id).blocks.all()
    except:
        raise Http404("Такого занятия нет")
    if request.method == 'POST':
        if 'Add-block' in request.POST:
            type_block=int(request.POST['type-block'])
            name_block=request.POST['name-block']
            lesson.blocks.add(TaskGroup.objects.create(name=name_block,local=type_block))
            #полный калл 
        elif 'Settings-lesson' in  request.POST:
            teacher_id=int(request.POST['id-teacher-lesson'])
            name_lesson = request.POST['name-lesson']
            date = request.POST['date']
            if 'open' in request.POST:
                lesson.open = True
            else:
                lesson.open = False
            lesson.teacher = User.objects.get(id=teacher_id)
            lesson.name = name_lesson
            if date != '':
                lesson.date=date
            lesson.save()
        elif 'Settings-Block' in request.POST:
            block_id=int(request.POST['block_id'])
            name_block = request.POST['name-block']
            type_block = request.POST['type-block']
            date_open = request.POST['date_open']
            date_part_close = request.POST['date_part_close']
            date_close = request.POST['date_close']
            task_group = TaskGroup.objects.get(id=block_id)
            if 'open' in request.POST:
                task_group.open = True
            else:
                task_group.open = False
            task_group.name = name_block
            task_group.local = type_block
            if date_open != '':
                task_group.date_open = date_open
            if date_part_close != '':
                task_group.date_part_close = date_part_close
            if date_close != '':
                task_group.date_close=date_close
            task_group.save()
    return render(request,'lesson_setting.html',context)

@staff_member_required
def delete_block(request, course_id, lesson_id,block_id):
    context = {'menu': get_context_menu(request, HOME_PAGE_NAME)} #заменить
    try:
        TaskGroup.objects.get(id=block_id).delete()
        context['lesson']=Lesson.objects.get(id=lesson_id)
        context['course']=Course.objects.get(id=course_id)
        context['blocks']=Lesson.objects.get(id=lesson_id).blocks.all()
    except:
        raise Http404("Такого занятия нет")
    path='/course/'+str(course_id)+'/'+str(lesson_id)+'/settings'
    return redirect(path)