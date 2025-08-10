from rest_framework import serializers
from order.models import Cart, CartItem, Order, OrderItem
from menu.models import FoodItem
from order.services import OrderService

class EmptySerializer(serializers.Serializer):
    pass

class SimpleFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'price', 'discount_price', 'is_special']

class AddCartItemSerializer(serializers.ModelSerializer):
    food_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['id', 'food_id', 'quantity']

    def validate_food_id(self, value):
        if not FoodItem.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Food not found.")
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        food_id = self.validated_data['food_id']
        quantity = self.validated_data['quantity']
        try:
            item = CartItem.objects.get(cart_id=cart_id, food_id=food_id)
            item.quantity += quantity
            item.save()
            self.instance = item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, food_id=food_id, quantity=quantity
            )
        return self.instance

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class CartItemSerializer(serializers.ModelSerializer):
    food = SimpleFoodSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'food', 'quantity', 'total_price']

    def get_total_price(self, obj):
        price = obj.food.discount_price if obj.food.is_special and obj.food.discount_price else obj.food.price
        return price * obj.quantity

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'created_at']
        read_only_fields = ['user', 'created_at']

    def get_total_price(self, cart):
        total = 0
        for item in cart.items.select_related('food'):
            price = item.food.discount_price if item.food.is_special and item.food.discount_price else item.food.price
            total += price * item.quantity
        return total

class OrderItemSerializer(serializers.ModelSerializer):
    food = SimpleFoodSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'food', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_price', 'items', 'created_at']
        read_only_fields = ['user', 'total_price', 'created_at']

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart found with this ID.')
        if not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('Cart is empty.')
        return cart_id

    def create(self, validated_data):
        user_id = self.context['user_id']
        cart_id = validated_data['cart_id']
        try:
            order = OrderService.create_order(user_id=user_id, cart_id=cart_id)
            return order
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def to_representation(self, instance):
        return OrderSerializer(instance).data
    

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
