import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.db.models import Q, F
from django.shortcuts import HttpResponse
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.postgres.search import SearchQuery, SearchRank, \
                                        SearchVector
from django.core.paginator import Paginator

from core.models import Product, ApiService, Logo,  \
    HtmlTemplate, DownloadSoftware, ProductPackage, \
    Feedback, Endpoints, Transaction, User
from core.utils import get_product_object, fulfill_order
from core.tasks import send_email, create_click_obj, create_impresion_obj
from buyer.tasks import add_client_activity


if settings.STRIPE_LIVE_MODE:
    stripe.api_key = settings.STRIPE_LIVE_SECRET_KEY
else:
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
endpoint_secret = settings.DJSTRIPE_WEBHOOK_SECRET


def index(request): # landing page
    """LANDING PAGE"""
    return render(request, 'core/index.html')


def redirect_users(request):
    """
    REDIRECT USERS FROM LANDING PAGE
    """
    if request.user.is_authenticated:
        if request.user.mode == 'S':
            return redirect('seller:dashboard')
        if request.user.mode == 'B':
            return redirect('buyer:dashboard')
    else:
        return redirect('core:explore')


def explore(request): # this contains the list of products
    """
    FILTER PRODUCTS BY APPROVED
    INCREASE THE IMPRESSIONS OF EACH PRODUCT
    """
    products = Product.objects.filter(
        status='A',
    ).order_by(
        'review_average', 
        'review_count'
    )

    paginator = Paginator(products, per_page=15)
    page_number = int(request.GET.get('page', 1))
    paginated_products = paginator.get_page(page_number)
    create_impresion_obj.delay(list(
        paginated_products.object_list.values_list(
            'id', flat=True
        )
    ))

    return render(request, 'core/explore.html', {
        'products': paginated_products,
        "pages": range(1, paginator.num_pages+1),
        "page_number": page_number
    })


def about(request):
    """
    RETURN ABOUT PAGE
    """
    return render(request, 'core/about.html')


def search_product(request):
    """
    SEARCH PRODUCT:
    FILTERS PRODUCTS BY TITLE AND DESCRIPTION
    IF AUTHENTICATED: CREATE SEARCH QUERY
    """
    query = request.GET.get('query')
    products = Product.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query) | Q(status='A')
    ).order_by(
        'review_average', 
        'review_count'
    )

    paginator = Paginator(products, per_page=15)
    page_number = int(request.GET.get('page', 1))
    paginated_products = paginator.get_page(page_number)
    create_impresion_obj.delay(list(
        paginated_products.object_list.values_list(
            'id', flat=True
        )
    ))

    if request.user.is_authenticated:
        add_client_activity.delay(
            f"You Searched: {query}",
            request.user.id,
            reverse('core:product-search')+f'query={query}'
        )

    return render(request, 'core/search.html', {
        'products': paginated_products,
        'query': query,
        "page_number": page_number

    })


def view_product(request, slug):
    """
    VIEW PRODUCT:
    GET PRODUCT OBJECT
    INCREASE THE CLICK OF THE PRODUCT
    GET PRODUCT PACKAGES
    GET PRODUCT FEEDBACKS
    IF AUTHENTICATED: CREATE CLIENT ACTIVITY
    """
    product = get_object_or_404(Product, slug=slug)
    obj, template = get_product_object(product)
    package = ProductPackage.objects.filter(service=product)
    feedbacks = Feedback.objects.filter(package__service=product).order_by('-id')
    create_click_obj.delay([product.id])
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
    """
    GET USER OBJECT
    GET USER PRODUCTS
    GET PRODUCTS FEEDBACKS
    """
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
    """
    IF GET: RETURN PENDING PRODUCTS
    IF POST:
        GET ACTION AND PRODUCT ID
        UPDATE THE STATUS OF PRODUCT WITH ACTION ID
    """
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
    """USER BILLING: RETURN ALL THE USER TRANSACTIONS"""
    transactions = Transaction.objects.filter(
        user=request.user
    ).order_by('-id')
    return render(request, 'core/billing.html', {
        'transactions': transactions
    })


def notifications(request): # this contains the list of products
    """USER NOTIFICATIONS: RETURNS ALL THE USER NOTIFICATIONS"""
    return render(request, 'core/notifications.html')


def project_plan(request): # ONLY FOR DEVs
    """PROJECT PLAN: RETURNS THE STATIC PRODUCT PLAN DEVELOPED BY DEVELOPERS"""
    return render(request, 'core/plan.html')


@csrf_exempt
def stripe_webhook(request):
    """
    STRIPE WEBHOOK VIEW:
    VERIFY SIGNATURE
    IF EVENT COMPLETED: FULLFILL ORDER
    """
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
    elif event['type'] == 'charge.failed':
        print(f'Payment Error')
        failure_msg = event['data']['object']['failure_message']
        send_email.delay(
            'farzanulhaq123@gmail.com',
            'Payment Failed',
            f'Payment Failed: {failure_msg}'
        )
    return HttpResponse(status=200)


def product_analysis_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    packages = ProductPackage.objects.filter(service=product)
    return render(request, 'analysis/product.html', {
        'product': product,
        "packages": packages
    })


def user_analysis_view(request, username):
    user = get_object_or_404(User, username=username)
    total_sales = 0
    total_orders_count = 0
    total_products_count = 6
    recent_orders_count = 0
    return render(request, 'analysis/user.html', {
        'user': user,
        'total_sales': total_sales,
        'total_orders_count': total_orders_count,
        'total_products_count': total_products_count,
        'recent_orders_count': recent_orders_count
    })


def admin_dashboard_view(request):
    return render(request, 'core/admin-dashboard.html', {
    })