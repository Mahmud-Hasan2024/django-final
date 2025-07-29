from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from menu.models import Category, FoodItem
from menu.serializers import CategorySerializer, FoodItemSerializer
from menu.filters import FoodFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(food_count=Count('foods')).all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy', 'partial_update']:
            return [IsAdminUser()]
        return [AllowAny()]

class FoodItemViewSet(ModelViewSet):
    queryset = FoodItem.objects.select_related('category').all()
    serializer_class = FoodItemSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = FoodFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy', 'partial_update']:
            return [IsAdminUser()]
        return [AllowAny()]

    @action(detail=False, methods=['get'])
    def specials(self, request):
        qs = self.get_queryset().filter(is_special=True)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
