import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.db.models import Q, F
from django.shortcuts import HttpResponse
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

from core.models import Product, ApiService, Logo,  \
    HtmlTemplate, DownloadSoftware, ProductPackage, \
    Feedback, Endpoints, Transaction, User
from core.utils import get_product_object, fulfill_order
from buyer.tasks import add_client_activity


if settings.STRIPE_LIVE_MODE:
    stripe.api_key = settings.STRIPE_LIVE_SECRET_KEY
else:
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
endpoint_secret = settings.DJSTRIPE_WEBHOOK_SECRET


def index(request): # landing page
    """Landing Page"""
    ## COMMENTING FOR NOW
    # if request.user.is_authenticated:
    #     if request.user.mode == 'S':
    #         return redirect('seller:dashboard')
    #     if request.user.mode == 'B':
    #         return redirect('buyer:dashboard')
    # else:
    #     return render(request, 'core/index.html')
    return render(request, 'core/index.html')


def redirect_users(request):
    """REDIRECT USERS FROM LANDING PAGE"""
    if request.user.is_authenticated:
        if request.user.mode == 'S':
            return redirect('seller:dashboard')
        if request.user.mode == 'B':
            return redirect('buyer:dashboard')
    else:
        return redirect('core:explore')


def explore(request): # this contains the list of products
    """This contains the list of products"""
    products = Product.objects.filter(
        status='A'
    )
    products.update(impressions=F('impressions') + 1)
    return render(request, 'core/explore.html', {
        'products': products
    })


def about(request):
    return render(request, 'core/about.html')

def search_product(request):
    query = request.GET.get('query')
    products = Product.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query) | Q(status='A')
    )
    if request.user.is_authenticated:
        add_client_activity.delay(
            f"You Searched: {query}",
            request.user.id,
            reverse('core:product-search')+f'query={query}'
    )
    return render(request, 'core/search.html', {
        'products': products,
        'query': query
    })


def view_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product.clicks += 1
    product.save()
    obj, template = get_product_object(product)
    package = ProductPackage.objects.filter(service=product)
    feedbacks = Feedback.objects.filter(package__service=product).order_by('-id')
    if request.user.is_authenticated:
        is_packages_bought = [
            request.user.package_already_bought(p.id)
            if request.user.is_authenticated else None
            for p in package
        ]
        add_client_activity.delay(
            f"Viewed: {product.title}",
            request.user.id,
            reverse('core:product-view', kwargs={
                'slug': product.slug
            })
        )
    else:
        is_packages_bought = [False for p in package]
    packages_index = [i for i in range(len(is_packages_bought))]
    print(is_packages_bought)
    if product.product_type == 'A':
        endpoints = Endpoints.objects.filter(service=obj)
        return render(request, template, {
            'product': product,
            "obj": obj,
            "endpoints": endpoints,
            "packages": package,
            "feedbacks": feedbacks,
            "is_packages_bought": is_packages_bought,
            "packages_index": packages_index
        })
    else:
        return render(request, template, {
            'product': product,
            "obj": obj,
            "package": package,
            "feedbacks": feedbacks,
            "is_packages_bought": is_packages_bought,
            "packages_index": packages_index

        })


def view_user(request, username):
    user = User.objects.get(username=username)
    print(user)
    products = Product.objects.filter(owner__username=username, status='A')
    product_ids = products.values_list('id', flat=True)
    feedbacks = Feedback.objects.filter(
        package__service__id__in=product_ids
    ).order_by('-id')

    return render(request, "core/view-user.html", {
        "user": user,
        "products": products,
        "feedbacks": feedbacks
    })


def admins_product_reivew(request):
    products = Product.objects.filter(status='P').order_by('-id')

    if not request.user.is_staff:
        raise Http404

    if request.method == 'POST':
        print(request.POST)
        product = Product.objects.get(
            id=int(
                request.POST.get('product_id')
            )
        )
        if request.POST.get('action') == 'A':
            product.status = 'A'
        elif request.POST.get('action') == 'R':
            product.status = 'R'
        product.save()

    return render(request, 'core/admin-product-review.html', {
        'products': products
    })

def billing(request): # this contains the list of products
    """This contains all the transaction history of user"""
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'core/billing.html', {
        'transactions': transactions
    })


def notifications(request): # this contains the list of products
    """This contains all the notifications of user"""
    return render(request, 'core/notifications.html')


def project_plan(request): # ONLY FOR DEVs
    return render(request, 'core/plan.html')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
        event['data']['object']['id'],
        expand=['line_items'],
        )

        line_items = session.line_items
        # Fulfill the purchase...
        fulfill_order(
            session.metadata, 
            line_items['data'][0]['amount_total']/100
        )
    # Passed signature verification
    return HttpResponse(status=200)