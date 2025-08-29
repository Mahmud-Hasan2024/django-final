from django.utils.html import format_html
from django.contrib import admin
from menu.models import Category, FoodItem

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'is_special', 'discount_price', 'image_tag']
    list_filter = ['category', 'is_special']
    search_fields = ['name', 'description']
    readonly_fields = ['image_tag']

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" style="object-fit:cover;" />', obj.image.url)
        return "-"
    image_tag.short_description = "Preview"
