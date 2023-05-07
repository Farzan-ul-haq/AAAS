import datetime

from core.models import User, Product, ProductPackage, \
    ClientPackages, Transaction, Notification
from django.shortcuts import redirect

def generate_buyer_token(buyer):
    return f"{buyer.id}{datetime.datetime.now().isoformat().replace('-', '').replace(':', '').replace('.', '')}"

def complete_product_purchase(data):
    product_package = ProductPackage.objects.get(id=data['product_package_id'])
    buyer = User.objects.get(id=data['uid'])
    seller = product_package.service.owner
    
    if product_package.service.product_type == 'A':
        cp = ClientPackages.objects.create(
            package=product_package,
            user=buyer,
            token=generate_buyer_token(buyer)
        )
        print(cp)
        cp.normal_requests_left = cp.normal_requests_left + product_package.normal_requests
        cp.save()
    else:
        ClientPackages.objects.create(
            package=product_package,
            user=buyer,
            token="LIFETIME-TOKEN"
        )
    # SUBRACT AMOUNT FROM BUYER
    Transaction.objects.create(
        coins=product_package.price,
        user=buyer,
        content='Product Purchase',
        type=1
    )
    # ADD AMOUNT TO SELLER
    Transaction.objects.create(
        coins=product_package.price,
        user=seller,
        content=f'{buyer.username} purchased your product.',
        type=0
    )
