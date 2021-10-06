from django.http.response import Http404, HttpResponse
from django.shortcuts import render

# Create your views here.

def lesson_view(request, course_id, lesson_id):
    return HttpResponse("Hi")