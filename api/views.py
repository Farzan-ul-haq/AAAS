from datetime import datetime

from django.http import JsonResponse
from django.contrib.postgres.search import SearchQuery, SearchRank, \
                                        SearchVector
from django.db.models import Count
from core.models import Product, ProductPackage, BrochureTemplates, \
    ProductClick, ProductImpression
# Create your views here.


def statistical_analysis(request, product_type, title=""):
    """
    Filter Products By TITLE
    RANK BY review_average
    CONVERT OBJ TO JSON
    RETURN JSON IN RESPONSE
    """
    print(title)
    products = Product.objects.filter(
        product_type=product_type,
        status='A'
    ).annotate(
        rank=SearchRank(
            SearchVector('review_average'),
            SearchQuery(title)
        )
    ).order_by('-rank')

    data = []
    for product in products[:5]:
        if product_type == 'A': # api products
            data.append({
                "id":product.id,
                "title":product.title,
                "review_count": product.review_count,
                "packages":[
                    {
                        'price': package.price,
                        'requests':package.normal_requests,
                        'title': package.title
                    } for package in ProductPackage.objects.filter(
                        service=product
                    )
                ]
                })
        else: # Other Products
            data.append({
                "id":product.id,
                "title":product.title,
                "review_count": product.review_count,
                "price": ProductPackage.objects.filter(service=product).first().price
            })
    print(data)
    return JsonResponse(data, safe=False)


def brochure_templates(request, product_type):
    """
    RETURN BROCHURES OF THE PRODUCT TYPE
    CONVERT OBJ TO JSON
    """
    bts = BrochureTemplates.objects.filter(product_type=product_type)
    data = []
    for bt in bts:
        data.append({
            "id": bt.id,
            "image": bt.image.url,
            "primary_color": bt.primary_color,
            "secondary_color": bt.secondary_color
        })
    return JsonResponse(data, safe=False)


def product_activity(request, product_id, activity_type):
    if activity_type == 'clicks':
        obj = ProductClick
    elif activity_type == 'impressions':
        obj = ProductImpression
    else:
        return JsonResponse({})
    activities = obj.objects.filter(
        product__id=product_id,
        datestamp__gte=datetime(2023, 7, 1)
    ).values('datestamp').annotate(
        activity=Count("product")
    ).order_by('-datestamp')

    return JsonResponse(
        [{
            "date": i["datestamp"],
            activity_type: i['activity']
        } for i in activities], safe=False
    )
