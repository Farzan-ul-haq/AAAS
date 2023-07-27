from django.contrib import admin
from django.urls import path, include

from . import views


app_name = 'api'

urlpatterns = [
    path('statistical-anaylsis/<str:product_type>/<str:title>/', views.statistical_analysis, name='statistical-analysis'),
    path('brochure-templates/<str:product_type>/', views.brochure_templates, name='brochure-templates'),

    path('products/<int:product_id>/feedback/', views.UserProductFeedbackView.as_view(), name='product-feedback'),
    path('products/<int:product_id>/orders/', views.UserProductFeedbackView.as_view(), name='product-orders'),
    path('products/<int:product_id>/<str:activity_type>/', views.product_activity, name='product-activity'),
    path('users/<str:username>/products/', views.UserProductsView.as_view(), name='user-products'),
    path('products/', views.UserProductsView.as_view(), name='products'),
]
