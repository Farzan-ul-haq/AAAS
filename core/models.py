import re
import requests

from tinymce.models import HTMLField

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
    ('H', 'TEMPLATE'),
    ('D', 'Software'), # desktop or mobile application.
)

class Category(models.Model):
    product_type = models.CharField(choices=PRODUCT_TYPES, default='A', max_length=1)
    name = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.product_type}: {self.name}"

    class Meta:
        db_table = "Category"


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = "Tag"

class Product(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    slug = models.CharField(default="", max_length=255, blank=True)
    description = HTMLField()
    
    thumbnail = models.ImageField('products/', null=True, blank=True)
    thumbnail_metadata = models.JSONField(null=True, blank=True)

    source_url = models.CharField(max_length=5000, null=True, blank=True)

    product_type = models.CharField(choices=PRODUCT_TYPES, default='A', max_length=1)

    last_approval_request_date = models.DateTimeField(auto_now=True)
    review_count = models.IntegerField(default=0)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    marketed_on = models.ManyToManyField('MarketingPlatforms', blank=True)

    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)

    status = models.CharField(choices=(
        ('A', 'approved'),
        ('R', 'rejected'),
        ('P', 'pending'),
        ('D', 'draft'),
    ), default='D', max_length=1)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Product"

    def __str__(self):
        return f"{self.product_type} | {self.owner.username} | {self.title}"

    def save(self, *args, **kwargs):
        self.slug = f"{self.id}-{self.title.replace(' ', '-').lower()}"
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return "/{self.user.username}/{self.slug}/"

class Logo(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    source_file = models.FileField('logo/')
    source_file_size = models.CharField(max_length=50, null=True, blank=True)
    width = models.IntegerField(default=0, null=True, blank=True)
    height = models.IntegerField(default=0, null=True, blank=True)
    logo_type = models.CharField(choices=(
        ('PORTAIT', 'PORTAIT'),
        ('LANDSCAPE', 'LANDSCAPE'),
        ('SQUARE', 'SQUARE'),
    ), max_length=100, default='SQUARE')

    class Meta:
        db_table = "Logo"


class HtmlTemplate(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    source_file = models.FileField('templates', null=True)
    source_file_size = models.CharField(max_length=50, null=True, blank=True)
    supported_browser = models.CharField(max_length=5000, null=True, blank=True)
    demo_site = models.CharField(max_length=5000, null=True, blank=True)
    technical_instructions = HTMLField(default="", null=True, blank=True)

    class Meta:
        db_table = "HtmlTemplate"


class DownloadSoftware(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    source_file = models.FileField('software', null=True)
    source_file_size = models.CharField(max_length=50, null=True, blank=True)
    in_scope = HTMLField(default="", null=True, blank=True)
    out_scope = HTMLField(default="", null=True, blank=True)
    technical_instructions = HTMLField(default="", null=True, blank=True)
    technology = models.CharField(default="", null=True, blank=True, max_length=500)
    trail_version = models.FileField('software-trail', null=True)

    supported_os = models.CharField(max_length=500, null=True, blank=True)
    software_type = models.CharField(choices=(
        ("OFFLINE", "OFFLINE"),
        ("ONLINE", "ONLINE"),
    ), max_length=100, default='ONLINE')

    class Meta:
        db_table = "DownloadSoftware"



class ApiService(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    website_url = models.CharField(max_length=5000) # website, optional
    base_url = models.CharField(max_length=5000) # API hosted server domain path
    in_scope = HTMLField(default="", null=True, blank=True)
    out_scope = HTMLField(default="", null=True, blank=True)
    technology = models.CharField(default="", null=True, blank=True, max_length=500)
    technical_instructions = HTMLField(default="", null=True, blank=True)

    def save(self, *args, **kwargs):
        super(ApiService, self).save(*args, **kwargs)

    class Meta:
        db_table = "ApiService"


class Endpoints(models.Model):
    path = models.CharField(max_length=5000)
    documentation = HTMLField(default="", null=True, blank=True)
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
    token = models.CharField(max_length=255)

    tiny_requests_left = models.IntegerField(default=0)
    normal_requests_left = models.IntegerField(default=0)
    last_request_used = models.DateTimeField(auto_now=True)

    reactivation = models.IntegerField(default=0) # show how many times the package is reactivated.
    timestamp = models.DateField(auto_now_add=True, null=True)

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
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "Feedback"


class Transaction(models.Model):
    type = models.IntegerField(default=0, choices=(
        (0, 'ADDED'),
        (1, 'SUBRACTED'),
    ))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    content = models.CharField(max_length=5000, default="")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type}|{self.coins}|{self.user.username}"

    def save(self, *args, **kwargs):
        user = self.user
        if self.type == 0:
            user.wallet += self.coins
        else:
            user.wallet -= self.coins
        user.save()
        Notification.objects.create(
            user=self.user,
            content=self.content,
            redirect_url=""
        )
        return super().save(*args, **kwargs)

    class Meta:
        db_table = "Transaction"


class BrochureTemplates(models.Model):
    image = models.ImageField("brochure-templates/", default="", null=True, blank=True)
    product_type = models.CharField(choices=PRODUCT_TYPES, default='A', max_length=1)
    primary_color = models.CharField(max_length=100, default='black')
    secondary_color = models.CharField(max_length=100, default='black')

    class Meta:
        db_table = "BrochureTemplates"


class Brochure(models.Model):
    title = models.CharField(max_length=5000, default="")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField("brochure/")

    def __str__(self):
        return f"{self.id} | {self.product}"


    class Meta:
        db_table = "Brochure"


class MarketingPlatforms(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    supported_products = models.CharField(max_length=500)
    price = models.IntegerField(default=0)

    class Meta:
        db_table = "MarketingPlatforms"


class DribbleProduct(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    views = models.IntegerField(default=0)
    description = models.TextField()
    dribble_id = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField('market/dribble/', null=True, blank=True)
    tags = models.CharField(max_length=5000)
    status = models.CharField(max_length=1, choices=(
        ('P', 'PENDING'),
        ('A', 'APPROVED'),
    ), default='P')
    # created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'DribbleProduct'

    def get_absolute_url(self):
        return f"{settings.DRIBBLE_SHOTS_URL}{self.dribble_id}"
    
    def get_details(self):
        try:
            if self.status == 'A':
                html_text = requests.get(self.get_absolute_url()).text
                views = int(re.search(
                            r'"viewsCount":\s*([^"]+)',
                            html_text
                        ).group(1).replace(',', ''))
                likes = int(re.search(
                            r'"likesCount":\s*([^"]+)',
                            html_text
                        ).group(1).replace(',', ''))
                print(likes)
            else:
                views = '-'
                likes = '-'


        except Exception as e:
            print(self.id)
            views = '--'
            likes = '--'
        return [
            [views, 'eye'],
            [likes, 'thumbs-up']
        ]