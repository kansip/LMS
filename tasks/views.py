from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from lesson.models import Lesson
from tasks.models import TaskGroup
from course.models import Course
from LMS_settings.menu import get_context_menu, HOME_PAGE_NAME
from django.http.response import Http404

@staff_member_required
def create_task(request, course_id, lesson_id, block_id):
    context = {'menu': get_context_menu(request, HOME_PAGE_NAME)} #заменить3
    try:
        context['lesson']=Lesson.objects.get(id=lesson_id)
        context['course']=Course.objects.get(id=course_id)
        context['blocks']=TaskGroup.objects.get(id=block_id)
    except:
        raise Http404("Такого занятия нет")
    
    return render(request,'lesson.html',context)