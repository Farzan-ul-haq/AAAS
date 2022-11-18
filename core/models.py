from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
                                        PermissionsMixin
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from django.conf import settings

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=25, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    wallet = models.PositiveIntegerField(default=0)
    mode = models.CharField(choices=(
        ('S', 'seller'),
        ('B', 'buyer'),
    ), default='S', max_length=1)

    objects = UserManager()

    USERNAME_FIELD = 'username'


PRODUCT_TYPES = (
    ('A', 'API'),
    ('L', 'Logo'),
    ('H', 'HTML TEMPLATE'),
    ('D', 'Downloadable Software'), # desktop or mobile application.
)


class Product(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    slug = models.CharField(default="", max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField('products/', null=True, blank=True)

    product_type = models.CharField(choices=PRODUCT_TYPES, default='A', max_length=1)

    last_approval_request_date = models.DateTimeField(auto_now=True)
    review_count = models.IntegerField(default=0)
    # Tags

    status = models.CharField(choices=(
        ('A', 'approved'),
        ('R', 'rejected'),
        ('P', 'pending'),
        ('P', 'pending'),
    ), default='P', max_length=1)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Product"


class Logo(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    download_file = models.ImageField('logo', null=True)

    class Meta:
        db_table = "Logo"


class HtmlTemplate(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    download_file = models.FileField('templates', null=True)

    class Meta:
        db_table = "HtmlTemplate"


class DownloadSoftware(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    download_file = models.FileField('templates', null=True)

    class Meta:
        db_table = "DownloadSoftware"



class ApiService(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    website_url = models.CharField(max_length=5000) # website, optional
    api_domain_url = models.CharField(max_length=5000) # API hosted server domain path

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


class ProductPackage(models.Model):
    service = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    price = models.IntegerField(default=0)

    tiny_requests = models.IntegerField(default=0)
    normal_requests = models.IntegerField(default=0)


    class Meta:
        db_table = "ProductPackage"


class ClientPackages(models.Model):
    package = models.ForeignKey(ProductPackage, on_delete=models.SET_NULL, null=True)
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
    package = models.ForeignKey(ProductPackage, on_delete=models.CASCADE)
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