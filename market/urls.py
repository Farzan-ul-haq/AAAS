from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'market'

urlpatterns = [
    # path('product/<int:product_id>/brochure/', views.brochure_list, name='brochure-list'),
    path('product/<int:product_id>/brochure/<int:brochure_id>/', views.brochure_detail, name='brochure-detail'),
    path('product/<int:pk>/market/', views.marketing_platform_list, name='market-list'),
]
