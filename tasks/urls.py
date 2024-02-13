from django.urls import path
from tasks.views import *
urlpatterns = [
    path('course/<int:course_id>/<int:lesson_id>/<int:block_id>/create_task', create_task),
    path('course/<int:course_id>/<int:lesson_id>/<int:block_id>/<int:task_id>/delete_task', delete_task),
    path('verification/', verification_tasks),
]