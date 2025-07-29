from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Sum, F
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from order.models import OrderItem, Order
from reviews.models import Review
from menu.models import FoodItem

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAdminUser])
def dashboard_stats(request):
    now = timezone.now()
    week_ago = now - timedelta(days=7)

    orders_per_week = (Order.objects
                       .filter(created_at__gte=week_ago)
                       .count())

    liked_foods = (Review.objects
                   .values(food_id=F('food_id'))
                   .annotate(avg_rating=Sum('rating') / Count('id'), total=Count('id'))
                   .order_by('-avg_rating')[:5])

    trending_foods = (OrderItem.objects
                      .filter(order__created_at__gte=week_ago)
                      .values('food_id', 'food__name')
                      .annotate(total_qty=Sum('quantity'))
                      .order_by('-total_qty')[:5])

    return Response({
        "orders_last_week": orders_per_week,
        "mostly_liked_foods": list(liked_foods),
        "trending_foods": list(trending_foods)
    })
