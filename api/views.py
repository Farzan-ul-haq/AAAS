from django.shortcuts import render , redirect
from django.http import JsonResponse
from django.contrib.postgres.search import SearchQuery, SearchRank, \
                                        SearchVector

from core.models import Product, ProductPackage
# Create your views here.


def statistical_analysis(request, product_type, title=""):
    products = Product.objects.filter(
        product_type=product_type
    ).annotate(
        rank=SearchRank(
            SearchVector('review_count'),
            SearchQuery(title)
        )
    ).order_by('-rank')

    data = []
    for product in products:
        thumbnail = product.thumbnail_metadata[0]["data"]
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
    return JsonResponse(data, safe=False)
