from datetime import datetime
from datetime import date, timedelta

from django.http import JsonResponse
from django.contrib.postgres.search import SearchQuery, SearchRank, \
                                        SearchVector
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from core.models import Product, ProductPackage, BrochureTemplates, \
    ProductClick, ProductImpression, Feedback, ClientPackages, \
    Brochure, DribbleProduct, CoroloftProduct, PinterestProduct, User
from api.serializers import ProductSerializer, FeedbackSerializer, \
    OrderSerializer, BrochureSerializer, UserSerializer

def statistical_analysis(request, product_type, title=""):
    """
    Filter Products By TITLE
    RANK BY review_average
    CONVERT OBJ TO JSON
    RETURN JSON IN RESPONSE
    """
    print(title)
    products = Product.objects.filter(
        product_type=product_type,
        status='A'
    ).annotate(
        rank=SearchRank(
            SearchVector('review_average'),
            SearchQuery(title)
        )
    ).order_by('-rank')

    data = []
    for product in products[:5]:
        if product_type == 'A': # api products
            data.append({
                "id":product.id,
                "title":product.title,
                "review_count": product.review_count,
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
        else: # Other Products
            data.append({
                "id":product.id,
                "title":product.title,
                "review_count": product.review_count,
                "price": ProductPackage.objects.filter(service=product).first().price
            })
    print(data)
    return JsonResponse(data, safe=False)


def brochure_templates(request, product_type):
    """
    RETURN BROCHURES OF THE PRODUCT TYPE
    CONVERT OBJ TO JSON
    """
    bts = BrochureTemplates.objects.filter(product_type=product_type)
    data = []
    for bt in bts:
        data.append({
            "id": bt.id,
            "image": bt.image.url,
            "primary_color": bt.primary_color,
            "secondary_color": bt.secondary_color
        })
    return JsonResponse(data, safe=False)


def product_activity(request, product_id, activity_type):
    if activity_type == 'clicks':
        obj = ProductClick
    elif activity_type == 'impressions':
        obj = ProductImpression
    else:
        return JsonResponse({})
    activities = obj.objects.filter(
        product__id=product_id,
        datestamp__gte=datetime(2023, 7, 1)
    ).values('datestamp').annotate(
        activity=Count("product")
    ).order_by('-datestamp')

    return JsonResponse(
        [{
            "date": i["datestamp"],
            activity_type: i['activity']
        } for i in activities], safe=False
    )


class UserProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        if 'username' in self.kwargs.keys():
            products = Product.objects.filter(
                owner__username=self.kwargs['username']
            )
        else:
            products = Product.objects.all()
        products = products.order_by(
            'review_average',
            'review_count'
        )
        return products


class UserProductFeedbackView(APIView):
    serializer_class = FeedbackSerializer

    def get(self, request, product_id):
        feedbacks = Feedback.objects.filter(
            package__service__id=product_id
        )
        serializer = self.serializer_class(feedbacks, many=True)
        print(serializer.data)
        return Response(serializer.data)


class UserProductOrdersView(APIView):
    serializer_class = FeedbackSerializer

    def get(self, request, product_id):
        return Response({})


class UserRecentOrdersView(APIView):
    serializer_class = OrderSerializer

    def get(self, request, username):
        orders = ClientPackages.objects.filter(
            timestamp__gte=date.today()-timedelta(days=3),
            package__service__owner__username=username
        )
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data)


class UserOrdersView(APIView):
    serializer_class = OrderSerializer

    def get(self, request, username):
        orders = ClientPackages.objects.filter(
            timestamp__lte=date.today()-timedelta(days=3),
            package__service__owner__username=username
        )
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data)


class ProductOrdersView(APIView):
    serializer_class = OrderSerializer

    def get(self, request, product_id):
        orders = ClientPackages.objects.filter(
            package__service__id=product_id
        )
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data)


class UserBrochureView(APIView):
    serializer_class = BrochureSerializer

    def get(self, request, username):
        brochures = Brochure.objects.filter(
            product__owner__username=username
        )
        serializer = self.serializer_class(brochures, many=True)
        return Response(serializer.data)


class UserMarketingResults(APIView):

    def get(self, request, username):
        output = {}
        output['dribble'] = [
            {
                "id": obj.id,
                "title": obj.title,
                "image": obj.image.url,
                "details": obj.get_details(),
                "url": obj.get_absolute_url()
            } for obj in DribbleProduct.objects.filter(
            product__owner__username=username
        )]
        output['coroflot'] = [
            {
                "id": obj.id,
                "title": obj.product.title,
                "image": obj.image.url,
                "details": obj.get_details(),
                "url": obj.get_absolute_url()
            } for obj in CoroloftProduct.objects.filter(
            product__owner__username=username
        )]
        output['pinterest'] = [
            {
                "id": obj.id,
                "title": obj.title,
                "image": obj.image.url,
                "details": None,
                "url": obj.get_absolute_url()
            } for obj in PinterestProduct.objects.filter(
            product__owner__username=username
        )]
        return Response(output)


class OrdersView(APIView):
    serializer_class = OrderSerializer

    def get(self, request):
        orders = ClientPackages.objects.filter(
        ).order_by('-timestamp')
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data)


class ProductListView(APIView):
    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.all().order_by(
            '-review_average',
            '-review_count'
        )
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data)


class UserListView(APIView):
    serializer_class = UserSerializer

    def get(self, request):
        users = User.objects.all().order_by('-wallet')
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)
 

class BrochureListView(APIView):
    serializer_class = BrochureSerializer

    def get(self, request):
        brochure = Brochure.objects.all().order_by('-id')
        serializer = self.serializer_class(brochure, many=True)
        return Response(serializer.data)


class MarketingResultsListView(APIView):

    def get(self, request):
        output = {}
        output['dribble'] = [
            {
                "id": obj.id,
                "title": obj.title,
                "image": obj.image.url,
                "details": obj.get_details(),
                "url": obj.get_absolute_url()
            } for obj in DribbleProduct.objects.filter(status='A')]
        output['coroflot'] = [
            {
                "id": obj.id,
                "title": obj.product.title,
                "image": obj.image.url,
                "details": obj.get_details(),
                "url": obj.get_absolute_url()
            } for obj in CoroloftProduct.objects.filter(status='A')]
        output['pinterest'] = [
            {
                "id": obj.id,
                "title": obj.title,
                "image": obj.image.url,
                "details": None,
                "url": obj.get_absolute_url()
            } for obj in PinterestProduct.objects.filter(status='A')]
        return Response(output)