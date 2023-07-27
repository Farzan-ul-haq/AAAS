from rest_framework import serializers

from core.models import Product, Feedback


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
            'package',
            'content',
            'rating'
        ]


# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ClientPackages