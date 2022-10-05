from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
                                        PermissionsMixin
from django.contrib.auth import get_user_model
from django.conf import settings

from .managers import UserManager


REQUEST_LEVEL_CHOICES = (
        ('tiny', 'tiny'),
        ('normal', 'normal'),
    )

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    wallet = models.PositiveIntegerField(default=0)
    mode = models.CharField(choices=(
        ('S', 'seller'),
        ('B', 'buyer'),
    ), default='S', max_length=1)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class ApiService(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(default="")
    website_url = models.CharField(max_length=5000)
    api_domain_url = models.CharField(max_length=5000) # API hosted server domain path
    description = models.TextField()
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    review_count = models.IntegerField(default=0)

    status = models.CharField(choices=(
        ('A', 'approved'),
        ('R', 'rejected'),
        ('P', 'pending'),
    ), default='P', max_length=1)
    last_approval_request_date = models.DateTimeField(auto_now=True)
    # Tags

    def save(self, *args, **kwargs):
        super(ApiService, self).save(*args, **kwargs)


class Endpoints(models.Model):
    path = models.CharField(max_length=5000)
    documentation = models.TextField()
    service = models.ForeignKey(ApiService, on_delete=models.CASCADE)
    request_type = models.CharField(choices=(
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PATCH', 'PATCH'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
    ), default='P', max_length=6)
    request_level = models.CharField(choices=REQUEST_LEVEL_CHOICES)
    test_data = models.TextField() # TEST json data


class ApiPackage(models.Model):
    service = models.ForeignKey(ApiService, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    price = models.IntegerField(default=0)

    tiny_requests = models.IntegerField(default=0)
    normal_requests = models.IntegerField(default=0)


class ClientPackages(models.Model):
    pass
    # apipackage
    # user
    # tiny_requests_left
    # normal_requests_left
    # last_request_used


class Notification(models.Model):
    pass
    # user
    # notification text
    # redirect url


