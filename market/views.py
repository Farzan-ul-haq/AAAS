import time
import chromedriver_autoinstaller
from selenium import webdriver

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.html import format_html
from core.models import Product, MarketingPlatforms, DribbleProduct


# Create your views here.
def brochure_list(request):
    """Returns Brochure List"""
    return render(request, 'market/brochure-list.html')

def brochure_detail(request, pk):
    """Returns Brochure Detail"""
    return render(request, 'market/brochure-detail.html')

def marketing_platform_list(request, pk):
    """Returns Marketing Platforms"""
    product = Product.objects.get(id=pk)
    print(product.marketed_on.all())
    if request.method == 'POST':
        platform = request.POST.get('platform')
        
    market_platforms = MarketingPlatforms.objects.all()
    return render(request, 'market/marketing-platform-list.html', {
        'product': product,
        "market_platforms": market_platforms
    })

def scraper(request):
    options = webdriver.ChromeOptions()
    options.add_argument(' - incognito')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=options)
    driver.get('https://google.com')
    file = driver.get_screenshot_as_base64()
    # DribbleProduct.objects.create('')
    driver.quit()
    return HttpResponse(format_html(f'<img src="data:;base64,{file}">'))
