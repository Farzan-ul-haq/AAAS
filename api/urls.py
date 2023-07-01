from django.contrib import admin
from django.urls import path, include

from . import views


app_name = 'api'

urlpatterns = [
    path('statistical-anaylsis/<str:product_type>/<str:title>/', views.statistical_analysis, name='statistical-analysis'),
    path('brochure-templates/<str:product_type>/', views.brochure_templates, name='brochure-templates'),
    path('product/<int:product_id>/<str:activity_type>/', views.product_activity, name='brochure-templates'),
]
