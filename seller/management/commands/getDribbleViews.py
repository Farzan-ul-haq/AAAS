import re
import requests
from lxml import html


from django.core.management.base import BaseCommand
from django.core.mail import send_mail

from django.conf import settings

REGEX_QUERY = r'"viewsCount":\s*([^"]+)'

class Command(BaseCommand):
    help = 'Get Information On Dribble Products'

    def get_dribble_url(self, dribble_product_id):
        return f"https://dribbble.com/shots/{dribble_product_id}"

    def get_views_count(self, html_text):
        return int(re.search(
            REGEX_QUERY, 
            html_text
        ).group(1).replace(',', ''))

    def handle(self, *args, **options):
        DRIBBLE_PRODUCT_ID = '20333170'

        views_count = self.get_views_count(
            html_text=requests.get(
                url=self.get_dribble_url(DRIBBLE_PRODUCT_ID)
            ).text
        )
        print(views_count)

