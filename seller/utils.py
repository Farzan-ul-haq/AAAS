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

def create_product_obj(*args, **data):
    data['status'] = 'A'
    return Product.objects.create(**data)


def create_endpoint_obj(*args, **data):
    return Endpoints.objects.create(**data)


def create_package_obj(*args, **data):
    ProductPackage.objects.create(**data)