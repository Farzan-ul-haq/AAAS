from django.shortcuts import render , redirect
from django.http import JsonResponse

from core.models import Product, ProductPackage
# Create your views here.


def statistical_analysis(request, product_type):
    products = Product.objects.filter(product_type=product_type)
    data = []
    for product in products:
        if product_type == 'A': # api products
            data.append([
                product.id,
                product.title,
                product.thumbnail.url,
                [[package.price, package.normal_requests, package.title] for package in \
                    ProductPackage.objects.filter(service=product)]
                ])
        else:
            data.append([
                product.id,
                product.title,
                product.thumbnail.url,
                ProductPackage.objects.filter(service=product).first().price
            ])
        return JsonResponse(data, safe=False)