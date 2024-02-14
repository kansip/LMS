from ctypes import resize
from itertools import chain
import re
import datetime
from typing import TYPE_CHECKING
from django.db.models import Q
from tasks.models import TaskGroup, Task, TaskTrueAnswers,TaskAnswers
from tasks.checker import *
from django.contrib.auth.models import Group, User
from lesson.models import Lesson
from lesson.tasks import open_lesson
from course.models import Course
from tasks.form import TaskForms
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render
from LMS_settings.menu import get_context_menu, HOME_PAGE_NAME
from LMS_settings.celery import app
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.storage import FileSystemStorage
# Create your views here.

@login_required
def lesson_view(request, course_id, lesson_id):
    """ Просмотр определенного занятия"""
    context = {'menu': get_context_menu(request, HOME_PAGE_NAME)} #заменить3
    try:
        context['lesson']=Lesson.objects.get(id=lesson_id)
        context['course']=Course.objects.get(id=course_id)
        context['blocks']=Lesson.objects.get(id=lesson_id).blocks.all()
        context['staff'] = request.user.is_staff
        if Lesson.objects.get(id=lesson_id).open == False and request.user.is_staff == 0:
            raise Http404("Занятие закрыто")
    except:
        raise Http404("Такого занятия нет")
    if len(Lesson.objects.get(id=lesson_id).blocks.all())==0:
        return render(request,'lesson.html',context)
    else:
        path="/course/"+str(course_id)+'/'+str(lesson_id)+"/"+str(Lesson.objects.get(id=lesson_id).blocks.all()[0].id)
        return redirect(path)

@login_required
def block_view(request, course_id, lesson_id,block_id):
    """ Просмотр определенного занятия"""
    context = {'menu': get_context_menu(request, HOME_PAGE_NAME)} #заменить3
    
    try:
        context['lesson']=Lesson.objects.get(id=lesson_id)
        context['course']=Course.objects.get(id=course_id)
        context['staff'] = request.user.is_staff 
        if request.user.is_staff:
            context['blocks']=Lesson.objects.get(id=lesson_id).blocks.all()
        else:
            context['blocks']=Lesson.objects.get(id=lesson_id).blocks.filter(open=1)
        if Lesson.objects.get(id=lesson_id).open == False and request.user.is_staff == 0:
            raise Http404("Занятие закрыто")
    except:
        raise Http404("Такого занятия нет")
    if request.method == 'POST':
        task_id=request.POST['task_id']
        task=Task.objects.get(id=task_id)
        if task.text_format_flag==1:
            answer=request.POST['answer']
            score=check(answer,task)
            taskans=TaskAnswers.objects.create(answer=answer,user=request.user,time=datetime.datetime.now(),score=score,task=task)
            taskans.save()
        else:
            answer = request.FILES['answer']
            fs = FileSystemStorage()
            filename = fs.save(answer.name, answer)
            taskans = TaskAnswers.objects.create(user=request.user,time=datetime.datetime.now(),score=0,task=task, files=answer)
            taskans.save()
    if (TaskGroup.objects.get(id=block_id).open)or request.user.is_staff:
        tasks=TaskGroup.objects.get(id=block_id).tasks.all()
    else:
        return render(request,'lesson.html',context)
    final_score=list()
    for i in range(len(tasks)):
        ans_task_user=TaskAnswers.objects.filter(task=tasks[i]).filter(user=request.user)
        pref_list=list()
        if len(ans_task_user)!=0:
            for j in range(len(ans_task_user)):
                pref_list.append(int(ans_task_user[j].score))
            final_score.append([tasks[i], max(pref_list)])
        else:
            final_score.append([tasks[i], 0])
    context['Tasks']=final_score
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
                open_lesson.apply_async((lesson_id,), eta=date)
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
        elif 'Added-Task' in request.POST:
                name_task = request.POST['name-task']
                cost_task = request.POST['cost-task']
                desc_task = request.POST['desc-task']
                radio_file_flag = request.POST['radio']
                answer = request.POST['answer']
                if 'rev_task' in request.POST:
                    rev_task = True
                else:
                    rev_task = False
                print(rev_task)
                task = 0
                if radio_file_flag == 'test':
                    task = Task.objects.create(name=name_task,cost=cost_task,desc=desc_task,revizion_format_flag=rev_task,file_format_flag=False,text_format_flag=True)
                    task.save()
                    answer=answer.split("\r\n")
                    for ans in answer:
                        TaskTrueAnswers.objects.create(true_flags=ans,task_id=task)
                elif radio_file_flag == 'text':
                    task = Task.objects.create(name=name_task,cost=0,desc=desc_task,revizion_format_flag=False,file_format_flag=False,text_format_flag=False)
                    task.save()
                else:
                    task = Task.objects.create(name=name_task,cost=cost_task,desc=desc_task,revizion_format_flag=True,file_format_flag=True,text_format_flag=False)
                    task.save()
                task_group = TaskGroup.objects.get(id=int(request.POST['block_id']))
                task_group.tasks.add(task)
                
    context['myform'] = TaskForms()
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

@staff_member_required
def results_block_view(request, course_id, lesson_id, block_id):
    context = {'menu': get_context_menu(request, HOME_PAGE_NAME)} #заменить
    try:
        context['lesson']=Lesson.objects.get(id=lesson_id)
        context['course']=Course.objects.get(id=course_id)
        context['blocks']=Lesson.objects.get(id=lesson_id).blocks.all()
        context['this_block'] = TaskGroup.objects.get(id=block_id)
    except:
        raise Http404("Такого занятия нет")
    users=Course.objects.get(id=course_id).students.user_set.all()
    tasks=TaskGroup.objects.get(id=block_id).tasks.filter(Q(file_format_flag=1) | Q(text_format_flag=1))
    context['tasks'] = tasks
    context['users'] = users
    final_score=list()
    for i in range(len(users)):
        score_tasks=list()
        for j in range(len(tasks)):
            ans_task_user=TaskAnswers.objects.filter(task=tasks[j]).filter(user=users[i])
            pref_list=list()
            if len(ans_task_user)!=0:
                for k in range(len(ans_task_user)):
                    pref_list.append(int(ans_task_user[k].score))
                score_tasks.append(max(pref_list))
            else:
                score_tasks.append(0)
        final_score.append([users[i], score_tasks, sum(score_tasks)])
    print(final_score)
    context['results']=final_score
    return render(request,'block_results.html',context)