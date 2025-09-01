from rest_framework import serializers
from menu.models import Category, FoodItem, FoodImage

class CategorySerializer(serializers.ModelSerializer):
    food_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'food_count']


class FoodImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodImage
        fields = ['id', 'image']

class FoodImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodImage
        fields = ['id', 'food', 'image']

class FoodItemSerializer(serializers.ModelSerializer):
    images = FoodImageSerializer(many=True, read_only=True)
    effective_price = serializers.SerializerMethodField()

    class Meta:
        model = FoodItem
        fields = [
            'id', 'name', 'description', 'price', 'is_special',
            'discount_price', 'effective_price', 'category', 'images'
        ]

    def get_effective_price(self, obj):
        return obj.effective_price
