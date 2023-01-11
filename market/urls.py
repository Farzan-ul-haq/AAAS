from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'market'

urlpatterns = [
    path('brochure/', views.brochure_list, name='brochure-list'),
    path('brochure/<int:pk>/', views.brochure_detail, name='brochure-detail'),
]
