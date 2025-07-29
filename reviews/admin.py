from django.contrib import admin
from reviews.models import Review

# Register your models here.

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'food', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['user__email', 'food__name', 'comment']

