from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'seller'

urlpatterns = [
    path('seller_dashboard/', views.seller_dashboard, name='dashboard'),
]
