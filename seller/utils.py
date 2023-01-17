from core.models import Product, Endpoints, ProductPackage


def create_product_obj(*args, **data):
    data['status'] = 'A'
    return Product.objects.create(**data)


def create_endpoint_obj(*args, **data):
    return Endpoints.objects.create(**data)


def create_package_obj(*args, **data):
    ProductPackage.objects.create(**data)