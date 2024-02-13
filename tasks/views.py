from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.db.models import Q
from lesson.models import Lesson
from tasks.models import TaskGroup,Task,TaskAnswers, TaskTrueAnswers
from course.models import Course
from LMS_settings.menu import *
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

@staff_member_required
def delete_task(request, course_id, lesson_id, block_id, task_id):
    context = {'menu': get_context_menu(request, HOME_PAGE_NAME)} #заменить3
    task = Task.objects.get(id=task_id)
    task.delete()
    path = "/course/"+ str(course_id)+'/'+str(lesson_id)+ "/settings"
    return redirect(path)


@staff_member_required
def verification_tasks(request):
    context = {'menu': get_context_menu(request, VERIFICATION_PAGE_NAME)}
    courses = Course.objects.filter(teacher=request.user)
    lessons=list()
    for course in courses:
        if Lesson.objects.filter(course=course).count()!=0:
            lessons.append(Lesson.objects.filter(course=course))
    blocks=list()
    for lesson_q in lessons:
        for lesson in lesson_q:
            for block in lesson.blocks.all():
                blocks.append(block)
    tasks=list()
    for block in blocks:
        for task in block.tasks.filter(revizion_format_flag=1):
            tasks.append(task)
    ans_and_tasks=list()
    for task in tasks:
        ans = TaskAnswers.objects.filter(Q(task=task) & Q(revizion=0))
        true_answer = TaskTrueAnswers.objects.filter(task_id=task)
        print(true_answer)
        if len(ans):
            ans_and_tasks.append([task,ans,true_answer])
    context["tasks"]=ans_and_tasks
    return render(request,"verification.html",context)