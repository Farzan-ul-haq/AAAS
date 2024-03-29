from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name='accounts'

urlpatterns = [
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('user_profile/',views.user_profile, name='user_profile'),
    path('user-mode-switch/',views.user_mode_switch, name='user-mode-switch'),

]
