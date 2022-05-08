"""LMS_settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from course.views import *
from django import urls
from django.urls import path

urlpatterns = [
    path('<int:course_id>', course_view),
    path('<int:course_id>/settings', course_settings),
    path('<int:course_id>/delete', course_delete),
    path('study', course_study_list),
    path('teaching', course_teaching_list),
    path('create',course_create),
]
