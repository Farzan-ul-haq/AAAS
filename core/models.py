from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
                                        PermissionsMixin
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

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
    slug = models.CharField(default="", max_length=255)
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


    class Meta:
        db_table = "ApiService"


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
    request_level = models.CharField(choices=(
        ('tiny', 'tiny'),
        ('normal', 'normal'),
    ), max_length=10)
    test_data = models.TextField() # TEST json data

    
    class Meta:
        db_table = "Endpoints"


class ApiPackage(models.Model):
    service = models.ForeignKey(ApiService, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    price = models.IntegerField(default=0)

    tiny_requests = models.IntegerField(default=0)
    normal_requests = models.IntegerField(default=0)

    
    class Meta:
        db_table = "ApiPackage"


class ClientPackages(models.Model):
    apipackage = models.ForeignKey(ApiPackage, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)

    tiny_requests_left = models.IntegerField(default=0)
    normal_requests_left = models.IntegerField(default=0)
    last_request_used = models.DateTimeField(auto_now=True)

    reactivation = models.IntegerField(0) # show how many times the package is reactivated.


    class Meta:
        db_table = "ClientPackages"


class Notification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    redirect_url = models.CharField(max_length=1000)


    class Meta:
        db_table = "Notification"


class Feedback(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    apipackage = models.ForeignKey(ApiPackage, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(5), 
            MinValueValidator(1)
        ]
    )


    class Meta:
        db_table = "Feedback"