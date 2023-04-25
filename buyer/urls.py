from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'buyer'

urlpatterns = [
    path('client_dashboard/', views.client_dashboard, name='dashboard'),
    path('buy_product/<int:price_package_id>/', views.buy_product, name='buy-product'),
]
