import re, base64
import requests
from datetime import datetime

from django.core.management.base import BaseCommand
from django.core.mail import send_mail

from django.conf import settings
from seller.utils import create_package_obj
from core.models import Product, User, Logo

REGEX_QUERY = r'"viewsCount":\s*([^"]+)'

class Command(BaseCommand):
    help = 'Bootstrap Code to Generate Users'

    def get_image_data(self, image_name):
        with open(image_name, "rb") as img_file:
            image_data = base64.b64encode(img_file.read())
        return image_data

    def handle(self, *args, **options):
        Product.objects.all().delete()

        user = User.objects.first()
        # logo Product
        logo1 = Product.objects.create(
            owner=user,
            product_type="L",
            title="Test Logo 1",
            description="<p>Test Description for Logo 1</p>",
            thumbnail_metadata=[
                {
                    'data': self.get_image_data('01.png'),
                    'is_primary': True
                },
                {
                    'data': self.get_image_data('02.png'),
                    'is_primary': False
                },
                {
                    'data': self.get_image_data('03.png'),
                    'is_primary': False
                },
            ],
            source_url = "https://google.com",
            review_count=0,
            status="A"
        )
        create_package_obj(
            service=logo1,
            title='BASIC',
            price=10,
        )
        Logo.objects.create(
            product=logo1,
            source_file=self.get_image_data("01.png"),
            source_file_size="0kb",
            width=10,
            height=10,
            logo_type="SQUARE"
        )

        logo2 = Product.objects.create(
            owner=user,
            product_type="L",
            title="Test Logo 2",
            description="<p>Test Description for Logo 2</p>",
            thumbnail_metadata=[
                {
                    'data': self.get_image_data("01.png"),
                    'is_primary': True
                }
            ],
            source_url = "https://google.com",
            review_count=0,
            status="A"
        )
        create_package_obj(
            service=logo2,
            title='BASIC',
            price=10,
        )
        Logo.objects.create(
            product=logo1,
            source_file=self.get_image_data("01.png"),
            source_file_size="0kb",
            width=10,
            height=10,
            logo_type="SQUARE"
        )
