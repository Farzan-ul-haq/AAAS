import json
from core.models import Product, Endpoints, ProductPackage


def update_product(product, request):
    product.title = request.POST.get('title')
    product.description = request.POST.get('description')
    product.source_url = request.POST.get('source_url')
    product.thumbnail_metadata = json.loads(request.POST.get('images'))
    product.save()
    return product

def create_product_obj(*args, **data):
    data['status'] = 'A'
    return Product.objects.create(**data)


def create_endpoint_obj(*args, **data):
    return Endpoints.objects.create(**data)


def create_package_obj(*args, **data):
    ProductPackage.objects.create(**data)