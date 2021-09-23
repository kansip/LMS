""" Роутинг, каким либо способом связанный с пользователем """
from django.urls import path
from .views import index, login_view, logout_view, main_page_view, register_view

urlpatterns = [
    path('', index),
    path('login/', login_view),
    path('register/', register_view),
    path('main/', main_page_view),
    path('logout/',logout_view)
]
