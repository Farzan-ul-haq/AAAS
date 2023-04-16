from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'seller'

urlpatterns = [
    path('seller_dashboard/', views.seller_dashboard, name='dashboard'),

    path('product/create/logo/', views.create_logo, name='create-logo'),
    path('product/create/template/', views.create_template, name='create-template'),
    path('product/create/software/', views.create_software, name='create-software'),
    path('product/create/api/', views.create_api, name='create-api'),

    path('product/delete/<int:product_id>/', views.delete_product, name='delete-product'),

]
