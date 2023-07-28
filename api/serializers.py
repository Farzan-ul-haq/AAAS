from rest_framework import serializers

from core.models import (
    Product, 
    Feedback, 
    ClientPackages,
    Brochure
)

class ProductSerializer(serializers.ModelSerializer):
    total_sales = serializers.SerializerMethodField()

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

            'total_sales'
        ]
    
    def get_total_sales(self, obj):
        return 0

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

    class Meta:
        model = ClientPackages
        fields = [
            "id",
            "amount_paid",
            "timestamp",
            "is_feedback_given",
            "feedback",
            "user"
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

    class Meta:
        model = Brochure
        fields = [
            'id',
            'title',
            'image_data',
        ]


# class MarketingPlatformsSerialier(serializers.Serializer):
    
    