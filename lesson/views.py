from ctypes import resize
from typing import TYPE_CHECKING
from tasks.models import TaskGroup
from lesson.models import Lesson
from course.models import Course
from lesson.forms import AddBlockForm
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render
from LMS_settings.menu import get_context_menu, HOME_PAGE_NAME
# Create your views here.

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

def settings(request, course_id, lesson_id):
    """ Настроек конкретного занятия <lesson_id> """
    context = {'menu': get_context_menu(request, HOME_PAGE_NAME)} #заменить
    try:
        lesson=Lesson.objects.get(id=lesson_id)
        context['lesson']=lesson
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
    return render(request,'lesson_setting.html',context)

def delete_block(request, course_id, lesson_id,block_id):
    context = {'menu': get_context_menu(request, HOME_PAGE_NAME)} #заменить
    TaskGroup.objects.get(id=block_id).delete()
    try:
        context['lesson']=Lesson.objects.get(id=lesson_id)
        context['course']=Course.objects.get(id=course_id)
        context['blocks']=Lesson.objects.get(id=lesson_id).blocks.all()
    except:
        raise Http404("Такого занятия нет")
    path='/course/'+str(course_id)+'/'+str(lesson_id)+'/settings'
    return redirect(path)