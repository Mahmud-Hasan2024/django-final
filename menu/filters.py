from django_filters.rest_framework import FilterSet
from menu.models import FoodItem

class FoodFilter(FilterSet):
    class Meta:
        model = FoodItem
        fields = {
            'category_id': ['exact'],
            'price': ['lt', 'gt'],
            'is_special': ['exact']
        }
