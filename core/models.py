import re
import requests
from bs4 import BeautifulSoup

from tinymce.models import HTMLField

from django.utils.timezone import now
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
    joining_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"{self.id} | {self.username} | {self.mode}"

    def package_already_bought(self, package_id):
        return ClientPackages.objects.filter(
            user=self,
            package__id=package_id
        ).exists()


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

    def __str__(self):
        return f"{self.id} | {self.name}"


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
    review_average = models.FloatField(default=0)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    marketed_on = models.ManyToManyField('MarketingPlatforms', blank=True)

    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    show_on_landing = models.BooleanField(default=False)

    status = models.CharField(choices=(
        ('A', 'approved'),
        ('R', 'rejected'),
        ('P', 'pending'),
        ('D', 'deleted'),
    ), default='D', max_length=1)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Product"

    def __str__(self):
        return f"{self.id} | {self.product_type} | {self.owner.username} | {self.title}"

    def save(self, *args, **kwargs):
        self.slug = f"{self.id}-{self.title.replace(' ', '-').lower()}"
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return "/{self.user.username}/{self.slug}/"

    def get_product_obj(self):
        if self.product_type == "A":
            obj = ApiService.objects.get(product=self)
        elif self.product_type == 'L':
            obj = Logo.objects.get(product=self)
        elif self.product_type == 'H':
            obj = HtmlTemplate.objects.get(product=self)
        elif self.product_type == 'D':
            obj = DownloadSoftware.objects.get(product=self)
        return obj

    def get_description_text(self):
        return BeautifulSoup(self.description, parser='lxml').text

    def get_dribble_obj(self):
        return DribbleProduct.objects.filter(product=self, status='A')
    
    def get_pinterest_obj(self):
        return PinterestProduct.objects.filter(product=self, status='A')

    def get_coroflot_obj(self):
        return CoroloftProduct.objects.filter(product=self, status='A')

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

    def __str__(self):
        return f"{self.id} | {self.product.title}"


class HtmlTemplate(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    source_file = models.FileField('templates', null=True)
    source_file_size = models.CharField(max_length=50, null=True, blank=True)
    supported_browser = models.CharField(max_length=5000, null=True, blank=True)
    demo_site = models.CharField(max_length=5000, null=True, blank=True)
    technical_instructions = HTMLField(default="", null=True, blank=True)

    class Meta:
        db_table = "HtmlTemplate"

    def __str__(self):
        return f"{self.id} | {self.product.title}"


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

    def __str__(self):
        return f"{self.id} | {self.product.title}"


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

    def __str__(self):
        return f"{self.id} | {self.product.title}"


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

    def get_full_test_url(self):
        return f"{settings.API_SERVER_TEST_URL}{self.path}"

    def __str__(self):
        return f"{self.id} | {self.service.product.title} | {self.path}"


class ProductPackage(models.Model):
    service = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    price = models.IntegerField(default=0)

    tiny_requests = models.IntegerField(default=0)
    normal_requests = models.IntegerField(default=0)


    class Meta:
        db_table = "ProductPackage"

    def __str__(self):
        return f"{self.id} | {self.service.title} | {self.title}"


class ClientPackages(models.Model):
    package = models.ForeignKey(ProductPackage, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    token = models.CharField(max_length=255)

    tiny_requests_left = models.IntegerField(default=0)
    normal_requests_left = models.IntegerField(default=0)
    last_request_used = models.DateTimeField(auto_now=True)

    reactivation = models.IntegerField(default=0) # show how many times the package is reactivated.
    timestamp = models.DateField(auto_now_add=True, null=True)
    is_feedback_given = models.BooleanField(default=False)

    class Meta:
        db_table = "ClientPackages"

    def __str__(self):
        return f"{self.id} | {self.package.service.title} | {self.user.username}"


class Notification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    redirect_url = models.CharField(max_length=1000)


    class Meta:
        db_table = "Notification"

    def __str__(self):
        return f"{self.id} | {self.user.username} | {self.content}"


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

    def __str__(self):
        return f"{self.id} | {self.rating} | {self.package.service.title} | {self.content}"

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
        if self.type == 0:
            return f"+ | {self.coins} | {self.user.username}"
        elif self.type == 1:
            return f"- | {self.coins} | {self.user.username}"


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


class ClientActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=5000)
    redirect_url = models.CharField(max_length=10000)

    def __str__(self):
        return f"{self.id} | {self.user.username} | {self.content}"


class BrochureTemplates(models.Model):
    image = models.ImageField("brochure-templates/", default="", null=True, blank=True)
    product_type = models.CharField(choices=PRODUCT_TYPES, default='A', max_length=1)
    primary_color = models.CharField(max_length=100, default='black')
    secondary_color = models.CharField(max_length=100, default='black')

    class Meta:
        db_table = "BrochureTemplates"

    def __str__(self):
        return f"{self.id} | {self.product_type} | {self.primary_color}"


class Brochure(models.Model):
    title = models.CharField(max_length=5000, default="")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_data = models.TextField(default="")


    def __str__(self):
        return f"{self.id} | {self.product.title}"


    class Meta:
        db_table = "Brochure"


class MarketingPlatforms(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    supported_products = models.CharField(max_length=500)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "MarketingPlatforms"


class DribbleProduct(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    description = models.TextField()
    dribble_id = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField('market/dribble/', null=True, blank=True)
    tags = models.CharField(max_length=5000)
    status = models.CharField(max_length=1, choices=(
        ('P', 'PENDING'),
        ('A', 'APPROVED'),
    ), default='P')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

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

    def __str__(self):
        return f"{self.id} | {self.status} | {self.dribble_id}"


class PinterestProduct(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    description = models.TextField()
    pinterest_id = models.CharField(max_length=255, blank=True, null=True)
    redirect_url = models.CharField(max_length=1000, blank=True, null=True)
    image = models.ImageField('market/pinterest/', null=True, blank=True)
    status = models.CharField(max_length=1, choices=(
        ('P', 'PENDING'),
        ('A', 'APPROVED'),
    ), default='P')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def get_absolute_url(self):
        return f"{settings.PINTEREST_PIN_URL}{self.pinterest_id}"

    def __str__(self):
        return f"{self.id} | {self.status} | {self.pinterest_id}"


class CoroloftProduct(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField()
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    coroflot_id = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField('market/coroflot/', null=True, blank=True)
    status = models.CharField(max_length=1, choices=(
        ('P', 'PENDING'),
        ('A', 'APPROVED'),
    ), default='P')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def get_absolute_url(self):
        return f"{settings.COROFLOT_PIN_URL}{self.coroflot_id}"

    def get_details(self):
        soup = BeautifulSoup(requests.get(self.get_absolute_url()).text)
        try: # VIEWS
            views = re.findall(
                "[0-9]+", soup.find_all("li", {"class": "stat_item"})[0].text
            )[0]
        except Exception as e:
            print(e)
            views = 0
        try:
            likes = re.findall(
                "[0-9]+", soup.find_all("li", {"class": "stat_item"})[1].text
            )[0]
        except Exception as e:
            print(e)
            likes = 0
        print(views)
        return [
            [views, 'eye'],
            [likes, 'thumbs-up'],
        ]

    def __str__(self):
        return f"{self.id} | {self.status} | {self.coroflot_id}"
