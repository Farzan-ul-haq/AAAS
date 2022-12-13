from django.contrib import admin
from django.urls import path

from . import views


app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('plan/', views.project_plan, name='project_plan'),
]
