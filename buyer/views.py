import stripe

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.urls import reverse

from core.models import ProductPackage, ClientPackages, Transaction, \
    Feedback, ClientActivity
# Create your views here.

def client_dashboard(request):
    bought_products = ClientPackages.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-id')
    activities = ClientActivity.objects.filter(user=request.user).order_by('-id')[:10]
    return render(request, 'buyer/dashboard.html', {
        "bought_products": bought_products,
        "transactions": transactions,
        'activities': activities
    })

def buy_product(request, price_package_id):
    domain_url = "http://" + request.get_host() 
    product_package = get_object_or_404(ProductPackage, pk=price_package_id)
    product = product_package.service
    if not request.user.is_authenticated:
        return redirect('accounts:login')
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


def give_feedback(request, bought_package_id):
    client_package = get_object_or_404(
        ClientPackages, 
        pk=bought_package_id, 
        is_feedback_given=False,
        user=request.user
    )

    if request.method == 'GET':
        return render(request, 'buyer/give-feedback.html', {
            "client_package": client_package
        })
    if request.method == 'POST':
        content = request.POST.get('content')
        rating = int(request.POST.get('rate'))
        f = Feedback.objects.create(
            user=request.user,
            package=client_package.package,
            content=content,
            rating=rating
        )

        client_package.is_feedback_given = True
        client_package.save()

        product = client_package.package.service
        product.review_count = product.review_count + 1
        product.review_average = (
            product.review_average + f.rating
        )/product.review_count
        product.save()
        
        return redirect('buyer:dashboard')