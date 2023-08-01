from django.contrib import admin
from django.urls import path, include

from . import views


app_name = 'api'

urlpatterns = [
    path('statistical-anaylsis/<str:product_type>/<str:title>/', views.statistical_analysis, name='statistical-analysis'),
    path('brochure-templates/<str:product_type>/', views.brochure_templates, name='brochure-templates'),

    path('users/<str:username>/products/', views.UserProductsView.as_view(), name='user-products'), #
    path('users/<str:username>/orders/', views.UserOrdersView.as_view(), name='user-orders'), #
    path('users/<str:username>/orders/recent/', views.UserRecentOrdersView.as_view(), name='user-recent-orders'), #
    path('users/<str:username>/brochures/', views.UserBrochureView.as_view(), name='user-brochures'), #
    path('users/<str:username>/market/', views.UserMarketingResults.as_view(), name='user-market'), #

    path('products/<int:product_id>/orders/', views.ProductOrdersView.as_view(), name='product-orders'),
    # path('products/<int:product_id>/feedback/', views.UserProductFeedbackView.as_view(), name='product-feedback'),
    path('products/<int:product_id>/<str:activity_type>/', views.product_activity, name='product-activity'),

    path('products/', views.ProductListView.as_view(), name='products'),
    path('orders/', views.OrdersView.as_view(), name='orders'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('brochures/', views.BrochureListView.as_view(), name='brochures'),
    path('market/', views.MarketingResultsListView.as_view(), name='market-results'),
]
