import time
import stripe
import chromedriver_autoinstaller
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from threading import Thread

from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.html import format_html
from core.models import Product, MarketingPlatforms, DribbleProduct, \
    Brochure, Notification
from market.utils import upload_product_to_dribble


if settings.STRIPE_LIVE_MODE:
    stripe.api_key = settings.STRIPE_LIVE_SECRET_KEY
else:
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
endpoint_secret = settings.DJSTRIPE_WEBHOOK_SECRET


# Create your views here.
def brochure_list(request):
    """Returns Brochure List"""
    return render(request, 'market/brochure-list.html')

def brochure_detail(request, pk):
    """Returns Brochure Detail"""
    return render(request, 'market/brochure-detail.html')

def brochure_detail2(request, pk=2):
    """Returns Brochure Details2"""
    return render(request, 'market/brochure-details2.html')

def brochure_detail3(request, pk):
    """Returns Brochure Details3"""
    return render(request, 'market/brochure-details3.html')


def marketing_platform_list(request, pk):
    """Returns Marketing Platforms"""
    product = Product.objects.get(id=pk)
    market_platforms = MarketingPlatforms.objects.all()
    brochures = Brochure.objects.filter(product=product)
    # IMAGES TO SHOW
    images = [[0, product.thumbnail]]
    image_counter = 0
    for brochure in brochures:
        image_counter += 1
        images.append([image_counter, brochure.image])

    if request.method == 'POST':
        platform = request.POST.get('platform')
        if platform == 'Dribble':
            selected_image = images[int(request.POST.get('selected_image'))][1]
            dp = DribbleProduct.objects.create(
                product=product,
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                tags=request.POST.get('tags'),
                image=selected_image,
                views=0,
                status='P'
            )
            price = MarketingPlatforms.objects.get(title=platform).price
            if price:
                pass
            else:
                Notification.objects.create(
                    user=request.user,
                    content="Your Product will be listed shortly on Dribble",
                )
                messages.warning(request, 'Your Product will be listed shortly on Dribble')
                t = Thread(
                    target=upload_product_to_dribble,
                    args=(
                        dp,
                        platform
                    )
                )
                t.start()
                return redirect('seller:dashboard')
        elif platform == 'Dribble-PRO':
            selected_image = images[int(request.POST.get('selected_image'))][1]
            dp = DribbleProduct.objects.create(
                product=product,
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                tags=request.POST.get('tags'),
                image=selected_image,
                views=0,
                status='P'
            )
            price = MarketingPlatforms.objects.get(title=platform).price
            if price:
                messages.warning(request, 'Your Product will be listed shortly on Dribble-PRO')
                # payment checkout URL
                checkout_session = stripe.checkout.Session.create(
                    line_items = [
                        {
                            'price_data': {
                                'currency': 'usd',
                                'unit_amount': int(price*100),
                                'product_data': {
                                    'name': f'Dribble PRO Listing',
                                },
                            },
                            'quantity': 1,
                        },
                    ],
                    metadata={
                        "uid": request.user.id,
                        "dribble_product": dp.id,
                        "platform": platform
                    },
                    mode='payment',
                    success_url=settings.DOMAIN_URL + reverse('seller:dashboard'),
                    cancel_url=settings.DOMAIN_URL + reverse('market:market-list', kwargs={'pk': pk}),
                )
                print(checkout_session.id)
                return redirect(checkout_session.url)
            else:
                Notification.objects.create(
                    user=request.user,
                    content="Your Product will be listed shortly on Dribble-PRO",
                )
                t = Thread(
                    target=upload_product_to_dribble,
                    args=(
                        dp,
                        platform
                    )
                )
                t.start()
                return redirect('seller:dashboard')
    else:
        return render(request, 'market/marketing-platform-list.html', {
            'product': product,
            "market_platforms": market_platforms,
            'images': images
        })

def scraper(request):
    options = webdriver.ChromeOptions()
    options.add_argument(' - incognito')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    i=1
    try:
        chromedriver_autoinstaller.install()
        driver = webdriver.Chrome(options=options)
        driver.get('https://google.com')
        file = driver.get_screenshot_as_base64()
        # DribbleProduct.objects.create('')
        driver.quit()
        return HttpResponse(format_html(f'<h1>{i}</h1><img src="data:;base64,{file}">'))
    except Exception as e:
        print(e)
    i=2
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get('https://google.com')
        file = driver.get_screenshot_as_base64()
        # DribbleProduct.objects.create('')
        driver.quit()
        return HttpResponse(format_html(f'<h1>{i}</h1><img src="data:;base64,{file}">'))
    except Exception as e:
        print(e)
