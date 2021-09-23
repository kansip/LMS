from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from LMS_settings.menu import get_context_menu, HOME_PAGE_NAME
# Create your views here.

@login_required
def course_view(request, course_id):
    context = {'menu': get_context_menu(request, HOME_PAGE_NAME)} 
    return render(request, 'course.html', context)