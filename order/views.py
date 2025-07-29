from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from order.serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, OrderSerializer
from order.models import Cart, CartItem, Order, OrderItem

# Create your views here.

class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def estimate_delivery(self, request, pk=None):
        cart = self.get_object()
        items_count = cart.items.count()
        return Response({"estimated_minutes": 30 + items_count * 2})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    @transaction.atomic
    def checkout(self, request, pk=None):
        cart = self.get_object()
        if cart.user != request.user and not request.user.is_staff:
            return Response({"detail": "Forbidden"}, status=403)

        if not cart.items.exists():
            return Response({"detail": "Cart is empty"}, status=400)

        order = Order.objects.create(user=request.user, total_price=0)
        total = 0
        for item in cart.items.select_related('food'):
            price = item.food.discount_price if item.food.is_special and item.food.discount_price else item.food.price
            OrderItem.objects.create(
                order=order, food=item.food, quantity=item.quantity, price=price
            )
            total += price * item.quantity

        order.total_price = total
        order.save()
        cart.items.all().delete()
        return Response(OrderSerializer(order).data)

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk'], 'request': self.request}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('food')

class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all().select_related('user').prefetch_related('items__food')
        return Order.objects.filter(user=self.request.user).select_related('user').prefetch_related('items__food')

    @action(detail=False, methods=['get'])
    def my(self, request):
        qs = self.get_queryset().filter(user=request.user)
        return Response(self.get_serializer(qs, many=True).data)

    def partial_update(self, request, *args, **kwargs):
        # allow admin to update status
        if not request.user.is_staff:
            return Response({"detail": "Only admins can update order status"}, status=403)
        return super().partial_update(request, *args, **kwargs)
