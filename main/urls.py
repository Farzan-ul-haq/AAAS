from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('seller.urls')),
    path('', include('buyer.urls')),
    path('user/', include('accounts.urls')),
    path('api/v1/', include('api.urls')),
]
