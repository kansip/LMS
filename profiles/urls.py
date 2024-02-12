""" Роутинг, каким либо способом связанный с пользователем """
from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('login/', login_view),
    path('register/', register_view),
    path('main/', main_page_view),
    path('logout/',logout_view),
    path('user/<int:user_id>', user_page_view),
    path('user/<int:user_id>/settings', user_settings_view),
    path('user/list', user_list_view)
]
