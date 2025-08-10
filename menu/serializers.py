from rest_framework import serializers
from menu.models import Category, FoodItem

class CategorySerializer(serializers.ModelSerializer):
    food_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'food_count']

class FoodItemSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    effective_price = serializers.SerializerMethodField()

    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'description', 'image', 'price', 'is_special', 'discount_price',
                  'effective_price', 'category']

    def get_effective_price(self, obj):
        return obj.effective_price
