from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

class FoodItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='foods')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = CloudinaryField('image')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_special = models.BooleanField(default=False)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

    @property
    def effective_price(self):
        return self.discount_price if self.is_special and self.discount_price else self.price
