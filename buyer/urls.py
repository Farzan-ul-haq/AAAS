from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'buyer'

urlpatterns = [
    path('client_dashboard/', views.client_dashboard, name='dashboard'),
]
