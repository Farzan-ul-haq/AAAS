from core.models import Product


def create_product(*args, **data):
    return Product.objects.create(**data)
