from django.contrib import admin
from django.urls import path

from . import views


app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('explore/', views.explore, name='explore'),
    path('billing/', views.billing, name='billing'),
    path('notifications/', views.notifications, name='notifications'),

    path('product/search/', views.search_product, name='product-search'),
    path('product/<str:slug>/', views.view_product, name='product-view'),

    path('user/<str:username>/', views.view_user, name='user-view'),

    path('plan/', views.project_plan, name='project_plan'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
]
