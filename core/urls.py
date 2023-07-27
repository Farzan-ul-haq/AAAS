from django.contrib import admin
from django.urls import path

from . import views


app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('redirect/', views.redirect_users, name='redirect'),
    path('explore/', views.explore, name='explore'),
    path('billing/', views.billing, name='billing'),
    path('about-us/', views.about, name='about-us'),
    path('notifications/', views.notifications, name='notifications'),

    path('product/search/', views.search_product, name='product-search'),
    path('product/<str:slug>/', views.view_product, name='product-view'),

    path('user/<str:username>/', views.view_user, name='user-view'),

    path('plan/', views.project_plan, name='project_plan'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),

    path('admins/product/review/', views.admins_product_reivew, name='admin-product-review'),
    path('admins/dashboard/', views.admin_dashboard_view, name='admin-dashboard'),

    path('analysis/product/<int:product_id>/', views.product_analysis_view, name='product-analysis'),
    path('analysis/user/<str:username>/', views.user_analysis_view, name='user-analysis'),
]
