import stripe

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.urls import reverse

from core.models import ProductPackage, ClientPackages, Transaction
# Create your views here.

def client_dashboard(request):
    bought_products = ClientPackages.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-id')

    return render(request, 'buyer/dashboard.html', {
        "bought_products": bought_products,
        "transactions": transactions
    })

def buy_product(request, price_package_id):
    domain_url = "http://" + request.get_host() 
    product_package = get_object_or_404(ProductPackage, pk=price_package_id)
    product = product_package.service
    # payment checkout URL
    checkout_session = stripe.checkout.Session.create(
        line_items = [
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(product_package.price*100),
                    'product_data': {
                        'name': f'Purchase: {product.title}',
                    },
                },
                'quantity': 1,
            },
        ],
        metadata={
            "uid": request.user.id,
            "product_package_id": product_package.id,
            'type': 'purchase_package'
        },
        mode='payment',
        success_url=domain_url + reverse('buyer:dashboard'),
        cancel_url=domain_url + reverse(
            'core:product-view', 
            kwargs={'slug': product.slug}
        ),
    )
    return redirect(checkout_session.url)