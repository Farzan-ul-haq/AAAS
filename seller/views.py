from django.shortcuts import render, redirect
from django.http import Http404

from core.models import Product, DownloadSoftware, Logo, \
    HtmlTemplate, ProductPackage, ApiService, Endpoints
from seller.utils import create_product


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
        p = create_product( # create product
            owner=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            thumbnail=request.FILES.get('thumbnail'),
            product_type='A',
        )

        apiservice = ApiService.objects.create( # create apiservice
            product=p,
            website_url='https://google.com',
            base_url="https://api.ipify.org/",
            in_scope="",
            out_scope="",
        )

        for i in range(len(request.POST.getlist('endpoint_url'))):
            Endpoints.objects.create(# create endpoints
                service=apiservice,
                path=request.POST.getlist('endpoint_url')[i],
                request_type=request.POST.getlist('endpoint_request_type')[i],
                request_level='tiny',
                documentation=request.POST.getlist('enpoint_desc')[i],
                test_data=request.POST.getlist('enpoint_test_data')[i],
            )
        
        for i in range(len(request.POST.getlist('package_requests'))):
            ProductPackage.objects.create(
                service=p,
                title=f"Package # {i}",
                normal_requests=request.POST.getlist('package_requests')[i],
                price=request.POST.getlist('package_pricing')[i],
            )
        return redirect('seller:dashboard')