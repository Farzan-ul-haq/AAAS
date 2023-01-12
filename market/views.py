from django.shortcuts import render
from core.models import Product, MarketingPlatforms

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
    market_platforms = MarketingPlatforms.objects.all()
    return render(request, 'market/marketing-platform-list.html', {
        'product': product,
        "market_platforms": market_platforms
    })
