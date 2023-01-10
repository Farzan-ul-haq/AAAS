from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.db.models import Q 

from core.models import Product, ApiService, Logo,  \
    HtmlTemplate, DownloadSoftware
from core.utils import get_product_object

def index(request): # landing page
    """Landing Page"""
    ## COMMENTING FOR NOW
    # if request.user.is_authenticated:
    #     if request.user.mode == 'S':
    #         return redirect('seller:dashboard')
    #     if request.user.mode == 'B':
    #         return redirect('buyer:dashboard')
    # else:
    #     return render(request, 'core/index.html')
    return render(request, 'core/index.html')

def explore(request): # this contains the list of products
    """This contains the list of products"""
    return render(request, 'core/explore.html', {
        'products': Product.objects.all()
    })


def search_product(request):
    query = request.GET.get('query')
    products = Product.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )
    return render(request, 'core/search.html', {
        'products': products,
        'query': query
    })


def view_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    obj, template = get_product_object(product)

    return render(request, template, {
        'product': product,
        "obj": obj,
    })


def billing(request): # this contains the list of products
    """This contains all the transaction history of user"""
    return render(request, 'core/billing.html')


def notifications(request): # this contains the list of products
    """This contains all the notifications of user"""
    return render(request, 'core/notifications.html')


def project_plan(request): # ONLY FOR DEVs
    return render(request, 'core/plan.html')
