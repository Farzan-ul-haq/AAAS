import io
import time
import stripe
import chromedriver_autoinstaller
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from threading import Thread
from datetime import datetime
import base64
from PIL import Image

from django.core.files.base import ContentFile
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.html import format_html
from django.views.decorators.csrf import csrf_exempt

from core.models import Product, MarketingPlatforms, DribbleProduct, \
    Brochure, Notification, \
    BrochureTemplates, PinterestProduct, CoroloftProduct
from core.utils import create_checkout_session, get_marketing_description
from market.tasks import upload_product_to_dribble, \
    upload_product_to_coroflot, upload_product_to_pinterest


if settings.STRIPE_LIVE_MODE:
    stripe.api_key = settings.STRIPE_LIVE_SECRET_KEY
else:
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
endpoint_secret = settings.DJSTRIPE_WEBHOOK_SECRET


# Create your views here.
def brochure_list(request):
    """Returns Brochure List"""
    bt = BrochureTemplates.objects.all()
    return render(request, 'market/brochure-list.html')

@csrf_exempt
def brochure_detail(request, product_id, brochure_id):
    """
    BROCHURE DETAIL:
    GET PRODUCT
    RETURN TO BROCHURE DETAIL
    """
    product = Product.objects.get(id=product_id)
    if request.method == 'GET':
        return render(request, 'market/brochure-detail.html', {
            'product': product
        })
    if request.method == 'POST':
        print(request.POST)
        image_data = request.POST['myCanvasData']
        print('========')
        print(image_data)
        if image_data:
            print('BROCHURE CREATED')
            b = Brochure.objects.create(
                title=product.title, product=product,
                image_data=image_data
            )
        return redirect('seller:dashboard')


def marketing_platform_list(request, pk):
    """
    MARKETING PLATFORM LIST:
    GET PRODUCT OBJECT
    GET MARKETING PLATFORMS
    GET BROCHURES
    GET LIST OF IMAGES(PRODUCT.THUMBNAIL + PRODUCT.BROCHURE)
    IF GET: 
        RETURN PLATFORM LIST
    IF POST:
        GET DOMAIN URL
        GET PLATFORM
        CREATE IMAGE
        CREATE INFO NOTIFICATION
        GET MARKETING PLATFORM PRICE
        GET MARKETING OBJ WITH STATUS "PENDING"
        IF PRICE:
            CREATE SUCCESS URL, CANCEL URL, METADATA & CREATE CHECKOUT SESSION
            REDIRECT TO STRIPE WEBHOOK PAGE
        ELSE:
            START MARKETING PLATFORM SCRIPT IN BACKGROUND
    """
    product = Product.objects.get(id=pk)
    market_platforms = MarketingPlatforms.objects.all()
    brochures = Brochure.objects.filter(product=product)
    # IMAGES TO SHOW
    images = []
    image_counter = 0
    for thumbnail in product.thumbnail_metadata:
        images.append([image_counter, thumbnail['data']])
        image_counter += 1
    for brochure in brochures:
        images.append([image_counter, brochure.image_data])
        image_counter += 1
    if request.method == 'GET':
        return render(request, 'market/marketing-platform-list.html', {
            'product': product,
            "market_platforms": market_platforms,
            'images': images
        })
    if request.method == 'POST':
        domain_url = "http://" + request.get_host()
        platform = request.POST.get('platform')
        print(request.POST)
        # GET SELECTED IMAGE
        selected_image_index = request.POST.get('selected_image')
        selected_image = images[int(selected_image_index)][1]
        format, imgstr = selected_image.split(';base64,')
        ext = format.split('/')[-1]
        c = ContentFile(base64.b64decode(imgstr))
        filename = "profile-"+datetime.now().strftime("%Y%m%d-%H%M%S")+"." + ext

        NOTIFICATION_MSG = f"Your product will be listed shortly on {platform}"
        messages.warning(request, NOTIFICATION_MSG)
        Notification.objects.create(
            user=request.user,
            content=NOTIFICATION_MSG,
        )
        price = MarketingPlatforms.objects.get(title=platform).price
        redirect_url = domain_url+reverse(
            'core:product-view', 
            kwargs={'slug': product.slug}
        )

        if platform.lower() == 'dribble':
            print('DRIBBLE==============')
            dp = DribbleProduct.objects.create(
                product=product,
                title=request.POST.get('title'),
                description=f"{request.POST.get('description')} {get_marketing_description(product.product_type, redirect_url)}",
                tags=request.POST.get('tags'),
                views=0,
                status='P'
            )
            dp.image.save(filename, c, save=True)

            if price:
                checkout_session_url = create_checkout_session(
                    price=price,
                    title="Dribble Listing",
                    metadata={
                        "uid": request.user.id,
                        "dribble_product": dp.id,
                        "platform": platform,
                        'type': 'product_marketing'
                    },
                    success_url=settings.DOMAIN_URL + reverse('seller:dashboard'),
                    cancel_url=settings.DOMAIN_URL + reverse('market:market-list', kwargs={'pk': pk})
                )
                return redirect(checkout_session_url)
            else:
                upload_product_to_dribble.delay(dp.id, platform)
                return redirect('seller:dashboard')

        elif platform.lower() == 'dribble-pro':
            print('DRIBBLE-PRO==============')
            dp = DribbleProduct.objects.create(
                product=product,
                title=request.POST.get('title'),
                description=f"{request.POST.get('description')} {get_marketing_description(product.product_type, redirect_url)}",
                tags=request.POST.get('tags'),
                views=0,
                status='P'
            )
            dp.image.save(filename, c, save=True)

            if price:
                checkout_session_url = create_checkout_session(
                    price=price,
                    title="Dribble PRO Listing",
                    metadata={
                        "uid": request.user.id,
                        "dribble_product": dp.id,
                        "platform": platform,
                        'type': 'product_marketing'
                    },
                    success_url=settings.DOMAIN_URL + reverse('seller:dashboard'),
                    cancel_url=settings.DOMAIN_URL + reverse('market:market-list', kwargs={'pk': pk})
                )
                return redirect(checkout_session_url)
            else:
                upload_product_to_dribble.delay(dp.id, platform)
                return redirect('seller:dashboard')

        elif platform == 'Pinterest':
            print('PINTEREST==============')
            pp = PinterestProduct.objects.create(
                product=product,
                title=request.POST.get('title'),
                description=f"{request.POST.get('description')} {get_marketing_description(product.product_type, redirect_url)}",
                pinterest_id='',
                redirect_url=redirect_url,
                status='P'
            )
            pp.image.save(filename, c, save=True)
            if price:
                checkout_session_url = create_checkout_session(
                    price=price,
                    title="Pinterest Listing",
                    metadata={
                        "uid": request.user.id,
                        "pinterest_product": pp.id,
                        "platform": platform,
                        'type': 'product_marketing'
                    },
                    success_url=settings.DOMAIN_URL + reverse('seller:dashboard'),
                    cancel_url=settings.DOMAIN_URL + reverse('market:market-list', kwargs={'pk': pk})
                )
                return redirect(checkout_session_url)
            else:
                upload_product_to_pinterest.delay(pp.id, platform)
                return redirect('seller:dashboard')
        elif platform == 'Coroflot':
            print('COROFLOT==============')
            cp = CoroloftProduct.objects.create(
                product=product,
                description=f"{request.POST.get('description')} {get_marketing_description(product.product_type, redirect_url)}",
                coroflot_id='',
                status='P'
            )
            cp.image.save(filename, c, save=True)
            if price:
                checkout_session_url = create_checkout_session(
                    price=price,
                    title="Coroflot Listing",
                    metadata={
                        "uid": request.user.id,
                        "coroflot_product": cp.id,
                        "platform": platform,
                        'type': 'product_marketing'
                    },
                    success_url=settings.DOMAIN_URL + reverse('seller:dashboard'),
                    cancel_url=settings.DOMAIN_URL + reverse('market:market-list', kwargs={'pk': pk})
                )
                return redirect(checkout_session_url)
            else:
                print(cp)
                upload_product_to_coroflot.delay(cp.id, platform)
                return redirect('seller:dashboard')