from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Sum, Avg
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from order.models import OrderItem, Order
from reviews.models import Review

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAdminUser])
def dashboard_stats(request):
    one_week_ago = timezone.now() - timedelta(days=7)

    recent_orders_count = Order.objects.filter(created_at__gte=one_week_ago).count()

    liked_reviews = (Review.objects.values('food_id').annotate(avg_rating=Avg('rating'), total_reviews=Count('id')).order_by('-avg_rating')[:5])

    trending_foods = OrderItem.objects.filter(order__created_at__gte=one_week_ago).values('food_id','food__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]

    return Response({
        'orders_last_week': recent_orders_count,
        'mostly_liked_foods': liked_reviews,
        'trending_foods': trending_foods,
    })