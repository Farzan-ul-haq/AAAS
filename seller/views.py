from django.shortcuts import render, redirect
from django.http import Http404

from core.models import Product, DownloadSoftware, Logo, \
    HtmlTemplate, ProductPackage

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
        print('PRODUCT SUBMITTED')
        return redirect('seller:dashboard')


def create_template(request):
    if request.method == 'GET':
        return render(
            request,
            'seller/create-template.html'
            )
    if request.method == 'POST':
        print('PRODUCT SUBMITTED')
        return redirect('seller:dashboard')


def create_software(request):
    if request.method == 'GET':
        return render(
            request,
            'seller/create-software.html'
            )
    if request.method == 'POST':
        title = request.POST.get('title')
        description= request.POST.get('description')
        thumbnail = request.FILES.get('thumbnail')
        downloadable_file = request.FILES.get('downloadable_file')
        price = int(request.POST.get('price'))

        p = Product.objects.create(
            title=title,
            description=description,
            thumbnail=thumbnail,
            product_type='D',
            owner=request.user
        )

        software = DownloadSoftware.objects.create(
            product=p,
            download_file=downloadable_file
        )
        ProductPackage.objects.create(
            service=p,
            title='BASIC',
            price=price
        )

        print('PRODUCT SUBMITTED')
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