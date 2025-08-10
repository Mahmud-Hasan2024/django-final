from django.urls import path, include
from rest_framework_nested import routers
from menu.views import CategoryViewSet, FoodItemViewSet
from order.views import CartViewSet, CartItemViewSet, OrderViewSet
from reviews.views import ReviewViewSet
from analytics.views import dashboard_stats

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('foods', FoodItemViewSet, basename='foods')
router.register('carts', CartViewSet, basename='carts')
router.register('orders', OrderViewSet, basename='orders')

food_router = routers.NestedDefaultRouter(router, 'foods', lookup='food')
food_router.register('reviews', ReviewViewSet, basename='food-reviews')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(food_router.urls)),
    path('', include(cart_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('analytics/dashboard/', dashboard_stats, name='dashboard-stats'),
    
]
