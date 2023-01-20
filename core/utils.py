from threading import Thread
from core.models import Product, ApiService, Logo, HtmlTemplate, \
    DownloadSoftware, DribbleProduct, Notification
from market.utils import upload_product_to_dribble

def get_product_object(product):
    if product.product_type == "A":
        obj = ApiService.objects.get(product=product)
        template_name = "core/view-api.html"
    elif product.product_type == 'L':
        template_name = "core/view-logo.html"
        obj = Logo.objects.get(product=product)
    elif product.product_type == 'H':
        template_name = "core/view-template.html"
        obj = HtmlTemplate.objects.get(product=product)
    elif product.product_type == 'D':
        template_name = "core/view-software.html"
        obj = DownloadSoftware.objects.get(product=product)
    return obj, template_name


def fulfill_order(data):
    if data['platform'].lower() == 'dribble':
        pass
    elif data['platform'].lower() == 'dribble-pro':
        dp = DribbleProduct.objects.get(id=data['dribble_product'])
        Notification.objects.create(
            user=dp.product.owner,
            content="Your Product will be listed shortly on Dribble-PRO",
        )
        t = Thread(
            target=upload_product_to_dribble,
            args=(
                dp,
                data['platform']
            )
        )
        t.start()