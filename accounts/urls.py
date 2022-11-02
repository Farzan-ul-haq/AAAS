from unicodedata import name
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('test/', views.test, name='test'),
    path('',views.base,name='base'),
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('logout/',views.login, name='logout'),

]
