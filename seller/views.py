import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from core.models import Product, DownloadSoftware, Logo, \
    HtmlTemplate, ProductPackage, ApiService, Endpoints, \
    Brochure, DribbleProduct, Transaction
from seller.utils import create_product_obj, create_endpoint_obj, \
    create_package_obj, update_product
from core.utils import get_product_object

def seller_dashboard(request):
    products = Product.objects.filter(owner=request.user)
    brochures = Brochure.objects.filter(product__owner=request.user).order_by('-id')
    dribble_product = DribbleProduct.objects.filter(product__owner=request.user)

    return render(request, 'seller/dashboard.html', context={
        'products': products,
        'brochures': brochures,
        'dribble_product': dribble_product,
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
            product_type='L',
            source_url=request.POST.get('source_url'),
        )
        p.thumbnail_metadata = json.loads(request.POST.get('images'))
        p.save()
        create_package_obj(
            service=p,
            title='BASIC',
            price=int(request.POST.get('price'))
        )
        Logo.objects.create(
            product=p,
            source_file=request.FILES.get('downloadable_file'),
            source_file_size=request.POST.get('source_file_size', '0kb'),
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
            product_type='H',
            source_url=request.POST.get('source_url', ""),
        )
        p.thumbnail_metadata = json.loads(request.POST.get('images'))
        p.save()
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
            technical_instructions=request.POST.get('technical_instructions'), #
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
            product_type='D',
            source_url="https://google.com",
        )
        p.thumbnail_metadata = json.loads(request.POST.get('images'))
        p.save()
        create_package_obj(
            service=p,
            title='BASIC',
            price=int(request.POST.get('price'))
        )
        DownloadSoftware.objects.create(
            product=p,
            source_file=request.FILES.get('downloadable_file'),
            trail_version=request.FILES.get('trail_version'),
            source_file_size=request.POST.get('source_file_size', '0kb'),
            in_scope=request.POST.get('in_scope'),
            out_scope=request.POST.get('out_scope'),
            supported_os=request.POST.get('supported_os'),
            software_type=request.POST.get('software_type', 'ONLINE'), # online, offline
            technical_instructions=request.POST.get('technical_instructions'),
            technology=request.POST.get('technology'),
        )
        return redirect('seller:dashboard')


def create_api(request):
    if request.method == 'GET':
        return render(
            request,
            'seller/create-api.html'
            )
    if request.method == 'POST':
        p = create_product_obj( # create product
            owner=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            thumbnail=request.FILES.get('thumbnail'),
            product_type='A',
            source_url=request.POST.get('source_url'),
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
            base_url=request.POST.get('base_url'),
            in_scope=request.POST.get('in_scope'),
            out_scope=request.POST.get('out_scope'),
            technical_instructions=request.POST.get('technical_instructions'),
        )
        for i in range(len(request.POST.getlist('endpoint_url'))):
            create_endpoint_obj(
                service=apiservice,
                path=request.POST.getlist('endpoint_url')[i],
                request_type=request.POST.getlist('endpoint_request_type')[i],
                request_level='normal',
                documentation=request.POST.getlist('enpoint_desc')[i],
                test_data=request.POST.getlist('enpoint_test')[i],
            )

        return redirect('seller:dashboard')

def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.owner != request.user:
        raise Http404
    print(product)
    if request.method == 'GET':
        return render(
            request,
            'seller/delete-product.html'
            )
    elif request.method == 'POST':
        product.delete()
        return redirect('seller:dashboard')

def update_logo(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    obj, template = get_product_object(product)
    package = get_object_or_404(ProductPackage, service=product)
    if product.owner != request.user:
        raise Http404
    if request.method == 'GET':
        return render(request, 'seller/create-logo.html', {
            'product': product,
            'obj': obj,
            'package': package
        })
    if request.method == 'POST':
        print(request.POST.get('width'))
        # UPDATE PRODUCT
        product = update_product(product, request)

        package.price = int(request.POST.get('price'))
        package.save()

        if "downloadable_file" in request.FILES.keys():
            print('FILE CHANGED')
            obj.source_file = request.FILES.get('downloadable_file')
        obj.width = request.POST.get('width')
        obj.height = request.POST.get('height')
        obj.logo_type = request.POST.get('logo_type')
        obj.save()

        return redirect('seller:dashboard')


def update_template(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    obj, template = get_product_object(product)
    package = get_object_or_404(ProductPackage, service=product)
    if product.owner != request.user:
        raise Http404
    if request.method == 'GET':
        return render(request, 'seller/create-template.html', {
            'product': product,
            'obj': obj,
            'package': package
        })
    if request.method == 'POST':
        product = update_product(product, request)

        package.price = int(request.POST.get('price'))
        package.save()

        if "downloadable_file" in request.FILES.keys():
            print('FILE CHANGED')
            obj.source_file = request.FILES.get('source_file')
        obj.technical_instructions = request.POST.get('technical_instructions')
        obj.supported_browser = request.POST.get('supported_browser')
        obj.demo_site = request.POST.get('demo_site')
        obj.save()

        return redirect('seller:dashboard')


def update_software(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    obj, template = get_product_object(product)
    package = get_object_or_404(ProductPackage, service=product)
    if product.owner != request.user:
        raise Http404
    if request.method == 'GET':
        return render(request, 'seller/create-software.html', {
            'product': product,
            'obj': obj,
            'package': package
        })
    if request.method == "POST":
        print(request.FILES)
        # UPDATE PRODUCT
        product = update_product(product, request)

        package.price = int(request.POST.get('price'))
        package.save()

        if "downloadable_file" in request.FILES.keys():
            obj.source_file = request.FILES.get('downloadable_file')

        if "trail_version" in request.FILES.keys():
            obj.trail_version = request.FILES.get('trail_version')

        obj.in_scope = request.POST.get('in_scope')
        obj.out_scope = request.POST.get('out_scope')
        obj.supported_os = request.POST.get('supported_os')
        obj.supported_browser = request.POST.get('supported_os')
        obj.software_type = request.POST.get('software_type', 'ONLINE')
        obj.technical_instructions = request.POST.get('technical_instructions')
        obj.technology = request.POST.get('technology')
        obj.save()

        return redirect('seller:dashboard')