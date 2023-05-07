import re, base64
import requests
from datetime import datetime

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.core.files import File

from django.conf import settings
from seller.utils import create_package_obj
from core.models import Product, User, Logo, MarketingPlatforms, \
    BrochureTemplates

REGEX_QUERY = r'"viewsCount":\s*([^"]+)'

class Command(BaseCommand):
    help = 'Bootstrap Code to Generate Users'


    def handle(self, *args, **options):
        self.create_marketing_platforms()
        self.create_users()
        self.create_brochure_templates()

        user = User.objects.first()
        # logo Product

    def create_marketing_platforms(self):
        MarketingPlatforms.objects.get_or_create(
            title="Dribble",
            supported_products="Logo, Web Template, Software, API Products",
        )
        MarketingPlatforms.objects.get_or_create(
            title="Dribble-PRO",
            supported_products="Logo, Web Template, Software, API Products",
        )
        MarketingPlatforms.objects.get_or_create(
            title="Pinterest",
            supported_products="Logo, Web Template, Software, API Products",
        )
        MarketingPlatforms.objects.get_or_create(
            title="Coroflot",
            supported_products="Logo, Web Template, Software, API Products",
        )

    def create_brochure_templates(self):
        bt = BrochureTemplates.objects.create(
            product_type='L',
            primary_color='blue',
            secondary_color='black', 
            image=File(open('static/b1.png', 'rb'))
        )
        bt = BrochureTemplates.objects.create(
            product_type='L',
            primary_color='black',
            secondary_color='black',
            image=File(open('static/b1-black.png', 'rb'))
        )

    def create_users(self):
        seller = User.objects.create_superuser(
            'admin-s',
            'admin3143',
            mode='S'
        )
        seller.save()

        buyer = User.objects.create_superuser(
            'admin-b',
            'admin3143',
            mode='B'
        )
        buyer.mode = 'B'
        buyer.save()