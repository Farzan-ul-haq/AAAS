import datetime

from django.shortcuts import redirect

from core.tasks import send_email
from core.models import User, Product, ProductPackage, \
    ClientPackages, Transaction, Notification

def generate_buyer_token(buyer):
    """
    GET BUYER ID
    GET THE DATEANDTIME
    GENERATE TOKEN BY ADDING THE BUYER ID + DATEANDTIME
    """
    return f"{buyer.id}{datetime.datetime.now().isoformat().replace('-', '').replace(':', '').replace('.', '')}"

def complete_product_purchase(data):
    """
    COMPLETE PRODUCT PURCHASE:
    GET PRODUCT PACKAGE
    GET PRODUCT BUYER
    GET SELLER
    CREATE CLIENT PACKAGE[SO USER CAN VIEW PRODUCT IN DASHBOARD]
    IF API PRODUCT:
        GENERATE TOKEN
        APPEND THE NO OF REUQESTS
    TRANSACTION LOG TO SUBRACT AMOUNT FROM BUYER
    TRANSACTION LOG TO ADD AMOUNT TO SELLER
    """
    product_package = ProductPackage.objects.get(id=data['product_package_id'])
    buyer = User.objects.get(id=data['uid'])
    seller = product_package.service.owner
    
    if product_package.service.product_type == 'A':
        cp = ClientPackages.objects.create(
            package=product_package,
            user=buyer,
            token=generate_buyer_token(buyer),
            amount_paid=product_package.price
        )
        cp.normal_requests_left = cp.normal_requests_left + product_package.normal_requests
        cp.save()
    else:
        ClientPackages.objects.create(
            package=product_package,
            user=buyer,
            token="LIFETIME-TOKEN",
            amount_paid=product_package.price,
        )
    # SUBRACT AMOUNT FROM BUYER
    Transaction.objects.create(
        coins=product_package.price,
        user=buyer,
        content='Product Purchase',
        type=1
    )
    send_email.delay(
        buyer.email,
        'Product Purchase Successful',
        f'Product Purchased successfully.\n{product_package.price}$ is subracted from your wallet.'
    )
    # ADD AMOUNT TO SELLER
    Transaction.objects.create(
        coins=product_package.price,
        user=seller,
        content=f'{buyer.username} purchased your product.',
        type=0
    )
    # SERVICE FEE SUBRACTING
    service_fee = product_package.price // 10
    Transaction.objects.create(
        coins=service_fee,
        user=seller,
        content=f'[SERVICE FEE] {buyer.username} purchased your product.',
        type=1
    )
    # ADD SERVICE FEE TO ADMIN ACCOUNT
    Transaction.objects.create(
        coins=service_fee,
        user=User.objects.get(username='admin'),
        content=f'{buyer.username} purchased your product.',
        type=0
    )
    send_email.delay(
        seller.email,
        'Product Purchase',
        f'{buyer.username} purchased your product.\n{product_package.price}$ is added to your wallet.'
    )
