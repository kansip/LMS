from tasks.models import TaskGroup, Task, TaskTrueAnswers,TaskAnswers

def check(user_answer, task):
    true_answer=TaskTrueAnswers.objects.filter(task_id=task)
    for i in range(len(true_answer)):
        if user_answer == true_answer[i].true_flags:
            return task.cost
    return 0