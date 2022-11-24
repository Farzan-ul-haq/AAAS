from django.shortcuts import render, redirect
from django.http import Http404

from core.models import Product, DownloadSoftware, Logo, \
    HtmlTemplate, ProductPackage
from seller.utils import create_product

PRODUCT_TYPES = ["API", 'LOGO', "TEMPLATE", "SOFTWARE"]

def seller_dashboard(request):
    return render(request, 'seller/dashboard.html', context={
        'products': Product.objects.all()
    })


def create_logo(request):
    if request.method == 'GET':
        return render(
            request,
            'seller/create-logo.html'
            )
    if request.method == 'POST':
        p = create_product(
            owner=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            thumbnail=request.FILES.get('thumbnail'),
            product_type='L',
        )
        Logo.objects.create(
            product=p,
            download_file=request.FILES.get('downloadable_file')
        )
        ProductPackage.objects.create(
            service=p,
            title='BASIC',
            price=int(request.POST.get('price'))
        )
        return redirect('seller:dashboard')


def create_template(request):
    if request.method == 'GET':
        return render(
            request,
            'seller/create-template.html'
            )
    if request.method == 'POST':
        p = create_product(
            owner=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            thumbnail=request.FILES.get('thumbnail'),
            product_type='H',
        )
        HtmlTemplate.objects.create(
            product=p,
            download_file=request.FILES.get('downloadable_file')
        )
        ProductPackage.objects.create(
            service=p,
            title='BASIC',
            price=int(request.POST.get('price'))
        )
        return redirect('seller:dashboard')


def create_software(request):
    if request.method == 'GET':
        return render(
            request,
            'seller/create-software.html'
            )
    if request.method == 'POST':
        p = create_product(
            owner=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            thumbnail=request.FILES.get('thumbnail'),
            product_type='D',
        )
        DownloadSoftware.objects.create(
            product=p,
            download_file=request.FILES.get('downloadable_file')
        )
        ProductPackage.objects.create(
            service=p,
            title='BASIC',
            price=int(request.POST.get('price'))
        )
        return redirect('seller:dashboard')


def create_api(request):
    if request.method == 'GET':
        return render(
            request,
            'seller/create-api.html'
            )
    if request.method == 'POST':
        print('PRODUCT SUBMITTED')
        return redirect('seller:dashboard')