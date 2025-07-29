from django.contrib import admin
from menu.models import Category, FoodItem

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'is_special', 'discount_price']
    list_filter = ['category', 'is_special']
    search_fields = ['name', 'description']
