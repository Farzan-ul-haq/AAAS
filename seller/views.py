from django.shortcuts import render, redirect
from django.http import Http404

from core.models import Product, DownloadSoftware, Logo, \
    HtmlTemplate, ProductPackage, ApiService, Endpoints
from seller.utils import create_product_obj, create_endpoint_obj, \
    create_package_obj


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
        p = create_product_obj(
            owner=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            thumbnail=request.FILES.get('thumbnail'),
            product_type='L',
            source_url=request.POST.get('source_url'),
        )
        create_package_obj(
            service=p,
            title='BASIC',
            price=int(request.POST.get('price'))
        )
        Logo.objects.create(
            product=p,
            source_file=request.FILES.get('downloadable_file'),
            source_file_size=request.POST.get('source_file_size'),
            width=request.POST.get('width'),
            height=request.POST.get('height'),
            logo_type=request.POST.get('logo_type')
        )
        return redirect('seller:dashboard')


def create_template(request):
    if request.method == 'GET':
        return render(
            request,
            'seller/create-template.html'
            )
    if request.method == 'POST':
        p = create_product_obj(
            owner=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            thumbnail=request.FILES.get('thumbnail'),
            product_type='H',
            source_url="https://google.com",
        )
        create_package_obj(
            service=p,
            title='BASIC',
            price=int(request.POST.get('price'))
        )
        HtmlTemplate.objects.create(
            product=p,
            source_file=request.FILES.get('downloadable_file'),
            source_file_size=request.POST.get('source_file_size'),
            supported_browser=request.POST.get('supported_browser'), #
            demo_site=request.POST.get('demo_site'), #
        )
        return redirect('seller:dashboard')


def create_software(request):
    if request.method == 'GET':
        return render(
            request,
            'seller/create-software.html'
            )
    if request.method == 'POST':
        p = create_product_obj(
            owner=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            thumbnail=request.FILES.get('thumbnail'),
            product_type='D',
            source_url="https://google.com",
        )
        create_package_obj(
            service=p,
            title='BASIC',
            price=int(request.POST.get('price'))
        )
        DownloadSoftware.objects.create(
            product=p,
            source_file=request.FILES.get('downloadable_file'),
            source_file_size=request.POST.get('source_file_size'),
            in_scope=request.POST.get('in_scope'),
            out_scope=request.POST.get('out_scope'),
            supported_os=request.POST.get('supported_os'),
            software_type=request.POST.get('software_type'), # online, offline
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
        p = create_product_obj( # create product
            owner=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            thumbnail=request.FILES.get('thumbnail'),
            product_type='A',
            source_url="https://google.com",
        )
        for i in range(len(request.POST.getlist('package_requests'))):
            create_package_obj(
                service=p,
                title=f"Package # {i}",
                normal_requests=request.POST.getlist('package_requests')[i],
                price=request.POST.getlist('package_pricing')[i],
            )

        apiservice = ApiService.objects.create( # create apiservice
            product=p,
            website_url='https://google.com',
            base_url="https://api.ipify.org/",
            in_scope="",
            out_scope="",
        )
        for i in range(len(request.POST.getlist('endpoint_url'))):
            create_endpoint_obj(
                service=apiservice,
                path=request.POST.getlist('endpoint_url')[i],
                request_type=request.POST.getlist('endpoint_request_type')[i],
                request_level='tiny',
                documentation=request.POST.getlist('enpoint_desc')[i],
                test_data=request.POST.getlist('enpoint_test_data')[i],
            )
        
        return redirect('seller:dashboard')