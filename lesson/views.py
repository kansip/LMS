from lesson.models import Lesson
from course.models import Course
from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from LMS_settings.menu import get_context_menu, HOME_PAGE_NAME
# Create your views here.

def lesson_view(request, course_id, lesson_id):
    """ Просмотр определенного занятия"""
    context = {'menu': get_context_menu(request, HOME_PAGE_NAME)} #заменить3
    try:
        context['lesson']=Lesson.objects.get(id=lesson_id)
        context['course']=Course.objects.get(id=course_id)
    except:
        return Http404("Такого занятия нет")
    return render(request,'lesson.html',context)