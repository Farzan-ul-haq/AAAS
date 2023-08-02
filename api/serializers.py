from datetime import datetime, timedelta

from rest_framework import serializers
from django.db.models import Sum
from core.models import (
    Product, 
    Feedback, 
    ClientPackages,
    Brochure,
    User,
    MarketingPlatforms
)

class MarketingPlatformsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = MarketingPlatforms
        fields = ['title']

class UserSerializer(serializers.ModelSerializer):
    total_sales = serializers.SerializerMethodField()
    recent_sales = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'wallet',
            
            'total_sales',
            'recent_sales'
        ]

    def get_total_sales(self, obj):
        total_sales = ClientPackages.objects.filter(
            package__service__owner=obj,
        ).aggregate(
            total_sales=Sum('amount_paid')
        )['total_sales']
        return total_sales if total_sales else 0

    
    def get_recent_sales(self, obj):
        total_sales = ClientPackages.objects.filter(
            package__service__owner=obj,
            timestamp__gte=datetime.today()-timedelta(days=3)
        ).aggregate(
            total_sales=Sum('amount_paid')
        )['total_sales']
        return total_sales if total_sales else 0


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
        ]


class ProductSerializer(serializers.ModelSerializer):
    total_sales = serializers.SerializerMethodField()
    recent_sales = serializers.SerializerMethodField()
    status = serializers.CharField(source='get_status_display')
    product_type = serializers.CharField(source='get_product_type_display')
    owner = UserInfoSerializer(read_only=True)
    marketed_on = MarketingPlatformsListSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'product_type',
            'title',
            'slug',
            'description',
            'thumbnail',
            'source_url',
            'review_count',
            'review_average',
            'marketed_on',
            'impressions',
            'clicks',
            'status',
            'created_at',
            'thumbnail',
            'owner',
            'marketed_on',

            'total_sales',
            'recent_sales',
        ]
    
    def get_total_sales(self, obj):
        total_sales = ClientPackages.objects.filter(
            package__service=obj
        ).aggregate(
            total_sales=Sum('amount_paid')
        )['total_sales']
        return total_sales if total_sales else 0

    
    def get_recent_sales(self, obj):
        total_sales = ClientPackages.objects.filter(
            package__service=obj,
            timestamp__gte=datetime.today()-timedelta(days=3)
        ).aggregate(
            total_sales=Sum('amount_paid')
        )['total_sales']
        return total_sales if total_sales else 0

class FeedbackSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Feedback
        fields = [
            'id',
            'username',
            'content',
            'rating'
        ]


class OrderSerializer(serializers.ModelSerializer):
    feedback = serializers.SerializerMethodField()
    product_title = serializers.CharField(source='package.service.title')
    product_thumbnail = serializers.ImageField(source='package.service.thumbnail')
    username = serializers.CharField(source='user.username')
    package_title = serializers.CharField(source='package.title')

    class Meta:
        model = ClientPackages
        fields = [
            "id",
            "amount_paid",
            "timestamp",
            "is_feedback_given",
            "feedback",
            "username",
            'product_title',
            'product_thumbnail',
            'package_title'
        ]

    def get_feedback(self, obj):
        feedback = Feedback.objects.filter(
                package=obj.package,
                user=obj.user
            )
        if feedback.exists():
            return FeedbackSerializer(
                feedback.first()
            ).data
        return None

class BrochureSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title')

    class Meta:
        model = Brochure
        fields = [
            'id',
            'title',
            'image_data',
            'product_title'
        ]


# class MarketingPlatformsSerialier(serializers.Serializer):
    
    