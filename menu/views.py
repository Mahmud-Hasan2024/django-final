from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from menu.models import FoodItem, Category
from menu.serializers import FoodItemSerializer, CategorySerializer
from menu.filters import FoodFilter
from menu.paginations import DefaultPagination
from api.permissions import IsAdminOrReadOnly
from rest_framework import viewsets, permissions
from menu.models import FoodImage
from menu.serializers import FoodImageUploadSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.

class FoodItemViewSet(ModelViewSet):
    serializer_class = FoodItemSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = FoodFilter
    pagination_class = DefaultPagination
    search_fields = ['name', 'description']
    ordering_fields = ['price']
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return FoodItem.objects.select_related('category').all()

    @swagger_auto_schema(operation_summary='Retrieve list of food items')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Create food item (Admin only)',
        operation_description='Admins can create a food item',
        request_body=FoodItemSerializer,
        responses={201: FoodItemSerializer, 400: 'Bad Request'}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='special', url_name='special')
    def special_foods(self, request):
        special_items = self.get_queryset().filter(is_special=True)
        serializer = self.get_serializer(special_items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='discounted', url_name='discounted')
    def discounted_foods(self, request):
        discounted_items = self.get_queryset().filter(discount_price__isnull=False)
        serializer = self.get_serializer(discounted_items, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='most-liked', url_name='most-liked')
    def most_liked_foods(self, request):
        queryset = self.get_queryset().annotate(total_reviews=Count('reviews')).filter(total_reviews__gt=0)
        queryset = queryset.order_by('-total_reviews')[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    

class FoodImageViewSet(viewsets.ModelViewSet):
    queryset = FoodImage.objects.all()
    serializer_class = FoodImageUploadSerializer
    permission_classes = [permissions.IsAdminUser]


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.annotate(food_count=Count('foods'))

    @swagger_auto_schema(operation_summary='Retrieve list of food categories')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Create category (Admin only)',
        operation_description='Admins can create food categories',
        request_body=CategorySerializer,
        responses={201: CategorySerializer, 400: 'Bad Request'}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
