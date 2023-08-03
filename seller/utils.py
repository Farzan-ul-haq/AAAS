import json
# from datetime import datetime
# import base64
# from django.core.files.base import ContentFile

from core.models import Product, Endpoints, ProductPackage, \
    Tag


def update_product(product, request):
    """
    UPDATE PRODUCT
    UPDATE THUMBNAIL IMAGES
    UPDATE TAGS
    """
    product.title = request.POST.get('title')
    product.description = request.POST.get('description')
    product.source_url = request.POST.get('source_url')
    product.thumbnail_metadata = json.loads(request.POST.get('images'))

    # selected_image = [i["data"] for i in product.thumbnail_metadata if i['isPrimary']][0]
    # format, imgstr = selected_image.split(';base64,')
    # ext = format.split('/')[-1]
    # c = ContentFile(base64.b64decode(imgstr))
    # filename = "product-"+datetime.now().strftime("%Y%m%d-%H%M%S")+"." + ext
    # product.thumbnail.save(filename, c, save=True)

    product.save()
    tags = [
        Tag.objects.get_or_create(
            name=tag.upper()
        )[0] for tag in json.loads(request.POST.get('tags'))
    ]
    product.tags.set(tags)
    return product

def create_product(request, request_type):
    """
    CREATE PRODUCT
    CREATE YHUMBNAIL IMAGES
    CREATE TAGS
    """
    p = create_product_obj(
        owner=request.user,
        title=request.POST.get('title'),
        description=request.POST.get('description'),
        product_type=request_type,
        source_url=request.POST.get('source_url'),
        thumbnail_metadata=json.loads(request.POST.get('images')),
    )
    # SAVE IMAGE
    # selected_image = [i["data"] for i in p.thumbnail_metadata if i['isPrimary']][0]
    # format, imgstr = selected_image.split(';base64,')
    # ext = format.split('/')[-1]
    # c = ContentFile(base64.b64decode(imgstr))
    # filename = "product-"+datetime.now().strftime("%Y%m%d-%H%M%S")+"." + ext
    # p.thumbnail.save(filename, c, save=True)

    p.save()
    tags = [
        Tag.objects.get_or_create(
            name=tag.upper()
        )[0] for tag in json.loads(request.POST.get('tags'))
    ]
    p.tags.set(tags)
    return p

def create_product_obj(*args, **data):
    """
    CREATE PRODUCT WITH STATUS "PENDING"
    """
    data['status'] = 'P'
    return Product.objects.create(**data)


def create_endpoint_obj(*args, **data):
    """
    CREATE ENDPOINT WITH DATA
    """
    return Endpoints.objects.create(**data)


def create_package_obj(*args, **data):
    """
    CREATE PRODUCT PACKAGE WITH DATA
    """
    ProductPackage.objects.create(**data)