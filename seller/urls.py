from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'seller'

urlpatterns = [
    path('seller_dashboard/', views.seller_dashboard, name='dashboard'),

    path('create/logo/', views.create_logo, name='create-logo'),
    path('create/template/', views.create_template, name='create-template'),
    path('create/software/', views.create_software, name='create-software'),
    path('create/api/', views.create_api, name='create-api'),

]
