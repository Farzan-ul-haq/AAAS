from django.shortcuts import render , redirect
from django.http import JsonResponse

from core.models import Product, ProductPackage
# Create your views here.


def statistical_analysis(request, product_type):
    products = Product.objects.filter(product_type=product_type)
    data = []
    for product in products:
        if product.thumbnail:
            thumbnail = product.thumbnail.url
        else:
            thumbnail = ""
        if product_type == 'A': # api products
            data.append({
                "id":product.id,
                "title":product.title,
                "thumbnail":thumbnail,
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
        else:
            data.append({
                "id":product.id,
                "title":product.title,
                "thumbnail":thumbnail,
                "price": ProductPackage.objects.filter(service=product).first().price
            })
        return JsonResponse(data, safe=False)