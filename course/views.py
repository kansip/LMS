from django.http.response import Http404
from course.models import Course
from lesson.models import Lesson
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required
from LMS_settings.menu import get_context_menu, HOME_PAGE_NAME
# Create your views here.

@login_required
def course_view(request, course_id):
    context = {'menu': get_context_menu(request, HOME_PAGE_NAME)} #заменить
    try:
        context['course']=Course.objects.get(id=course_id)
        context['lessons']=Lesson.objects.filter(course_id=course_id)
    except:
        raise Http404("There is no course with this id")
    return render(request, 'course.html', context)

@login_required
def course_study_list(request):
    context = {'menu': get_context_menu(request, HOME_PAGE_NAME)} #заменить

    return render(request, 'course.html', context)
