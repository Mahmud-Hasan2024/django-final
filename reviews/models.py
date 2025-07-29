from django.db import models
from django.conf import settings
from menu.models import FoodItem

# Create your models here.

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user', 'food']]
        ordering = ['-id']

    def __str__(self):
        return f"{self.user.email} -> {self.food.name} ({self.rating})"

