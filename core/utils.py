import stripe

from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect

from core.models import Product, ApiService, Logo, HtmlTemplate, \
    DownloadSoftware, DribbleProduct, Notification, Transaction, \
    User, CoroloftProduct, PinterestProduct
from market.tasks import upload_product_to_dribble, \
    upload_product_to_coroflot, upload_product_to_pinterest
from buyer.utils import complete_product_purchase
from core.tasks import send_email

if settings.STRIPE_LIVE_MODE:
    stripe.api_key = settings.STRIPE_LIVE_SECRET_KEY
else:
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
endpoint_secret = settings.DJSTRIPE_WEBHOOK_SECRET

CALL_TO_ACTIONS = {
    "A": "Accelerate your development process with our high-performance API - Buy now! {URL}",
    "L": "Accelerate your development process with our high-performance API - Buy now! {URL}",
    "H": "Upgrade your website's functionality with our feature-rich templates - Buy now! {URL}",
    "D": "Simplify your daily operations with our user-friendly software - Buy now! {URL}",
}

def get_marketing_description(product_type, redirect_url):
    """
    GET CALL TO ACTION ACCORDING TO THE PRODUCT TYPE
    """
    description = CALL_TO_ACTIONS[product_type]
    description = description.replace("{URL}", redirect_url)
    return description


def get_product_object(product):
    if product.product_type == "A":
        obj = ApiService.objects.get(product=product)
        template_name = "core/view-api.html"
    elif product.product_type == 'L':
        template_name = "core/view-logo.html"
        obj = Logo.objects.get(product=product)
    elif product.product_type == 'H':
        template_name = "core/view-template.html"
        obj = HtmlTemplate.objects.get(product=product)
    elif product.product_type == 'D':
        template_name = "core/view-software.html"
        obj = DownloadSoftware.objects.get(product=product)
    return obj, template_name


def fulfill_order(data, amount):
    """
    FULFILL ORDER
    CREATE TRANSACTION LOGS
    CHECK DATA
    IF TYPE == MARKETING
        MARKET ON THE PLATFORM
    IF TYPE == PRODUCT_PURCHSE
        COMPLETE PRODUCT PURCHASE
    """
    Transaction.objects.create(
        coins=amount,
        user=User.objects.get(id=data['uid']),
        content='Funds Added.',
        type=0
    )
    send_email.delay(
        User.objects.get(id=data['uid']).email,
        'Funds Added',
        f'Funds {amount}$ is added to your wallet'
    )
    if data['type'] == 'product_marketing':
        if data['platform'].lower() == 'dribble':
            obj = DribbleProduct.objects.get(id=data['dribble_product'])
            upload_product_to_dribble.delay(obj.id, data['platform'])
        elif data['platform'].lower() == 'dribble-pro':
            obj = DribbleProduct.objects.get(id=data['dribble_product'])
            upload_product_to_dribble.delay(obj.id, data['platform'])
        elif data['platform'].lower() == 'pinterest':
            obj = PinterestProduct.objects.get(id=data['dribble_product'])
            upload_product_to_pinterest.delay(obj.id, data['platform'])
        elif data['platform'].lower() == 'coroflot':
            obj = CoroloftProduct.objects.get(id=data['dribble_product'])
            upload_product_to_coroflot.delay(obj.id, data['platform'])
    elif data['type'] == 'purchase_package':
        print('+++++++++++')
        complete_product_purchase(data)

def create_checkout_session(price, title, metadata, success_url, cancel_url):
    """
    CREATE CHECKOUT SESSION
    """
    checkout_session = stripe.checkout.Session.create(
        line_items = [
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(price*100),
                    'product_data': {
                        'name': title,
                    },
                },
                'quantity': 1,
            },
        ],
        metadata=metadata,
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
    print(checkout_session.id)
    return checkout_session.url
