from django.urls import path
from tasks.views import *
urlpatterns = [
    path('<int:lesson_id>/<int:block_id>/create_task', create_task),
    path('<int:lesson_id>/<int:block_id>/<int:task_id>/delete_task', delete_task),
]