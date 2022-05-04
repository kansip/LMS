from django.urls import path
from tasks.views import *
urlpatterns = [
    path('<int:lesson_id>/<int:block_id>/create_task', create_task),
]