from django.db.models import Count, Sum, Avg
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from order.models import OrderItem, Order
from reviews.models import Review

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user

    if user.is_staff:
        total_orders = Order.objects.count()
        liked_reviews = (
            Review.objects.values("food_id", "food__name")
            .annotate(avg_rating=Avg("rating"), total_reviews=Count("id"))
            .order_by("-avg_rating")[:5]
        )
        trending_foods = (
            OrderItem.objects.values("food_id", "food__name")
            .annotate(total_quantity=Sum("quantity"))
            .order_by("-total_quantity")[:5]
        )

        return Response({
            "type": "admin",
            "total_orders": total_orders,
            "mostly_liked_foods": liked_reviews,
            "trending_foods": trending_foods,
        })

    orders = Order.objects.filter(user=user).order_by("-created_at")

    total_orders = orders.count()
    total_spent = orders.aggregate(total=Sum("total_price"))["total"] or 0
    last_order_date = orders.first().created_at if orders.exists() else None

    recent_orders = [
        {
            "id": order.id,
            "status": order.status,
            "total": order.total_price,
            "created_at": order.created_at,
        }
        for order in orders[:5]
    ]

    return Response({
        "type": "user",
        "total_orders": total_orders,
        "total_spent": float(total_spent),
        "last_order_date": last_order_date,
        "recent_orders": recent_orders,
    })
