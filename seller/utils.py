import json
from core.models import Product, Endpoints, ProductPackage, \
    Tag


def update_product(product, request):
    product.title = request.POST.get('title')
    product.description = request.POST.get('description')
    product.source_url = request.POST.get('source_url')
    product.thumbnail_metadata = json.loads(request.POST.get('images'))
    product.save()
    tags = [
        Tag.objects.get_or_create(
            name=tag
        )[0] for tag in json.loads(request.POST.get('tags'))
    ]
    product.tags.set(tags)
    return product

def create_product(request, request_type):
    p = create_product_obj(
        owner=request.user,
        title=request.POST.get('title'),
        description=request.POST.get('description'),
        product_type=request_type,
        source_url=request.POST.get('source_url'),
    )
    p.thumbnail_metadata = json.loads(request.POST.get('images'))
    p.save()
    tags = [
        Tag.objects.get_or_create(
            name=tag
        )[0] for tag in json.loads(request.POST.get('tags'))
    ]
    p.tags.set(tags)
    return p

def create_product_obj(*args, **data):
    data['status'] = 'P'
    return Product.objects.create(**data)


def create_endpoint_obj(*args, **data):
    return Endpoints.objects.create(**data)


def create_package_obj(*args, **data):
    ProductPackage.objects.create(**data)