from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('accounts.urls')),
    path('', include('core.urls')),
    path('', include('seller.urls')),
    path('', include('buyer.urls')),
    path('', include('market.urls')),

    path('api/v1/', include('api.urls')),

    path('tinymce/', include('tinymce.urls')),

    path(
        'reset_password/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html'
        ),
        name="reset_password"
    ),
    path(
        'reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_sent.html'
        ),
        name="password_reset_done"
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_form.html'
        ),
        name="password_reset_confirm"
    ),
    path(
        'reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_done.html'
        ),
        name="password_reset_complete"
    ),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/change_password.html',
            success_url = '/'
        ),
        name='change_password'
    ),


]+ static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
