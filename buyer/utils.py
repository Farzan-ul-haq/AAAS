from core.models import User, Product, ProductPackage, \
    ClientPackages, Transaction, Notification
from django.shortcuts import redirect


def complete_product_purchase(data):
    product_package = ProductPackage.objects.get(id=data['product_package_id'])
    buyer = User.objects.get(id=data['uid'])
    seller = product_package.service.owner
    
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
        type=0
    )
    # ADD AMOUNT TO SELLER
    Transaction.objects.create(
        coins=product_package.price,
        user=seller,
        content=f'{buyer.username} purchased your product.',
        type=1
    )
