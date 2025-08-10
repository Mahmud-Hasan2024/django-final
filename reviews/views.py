from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from reviews.models import Review
from reviews.serializers import ReviewSerializer

# Create your views here.

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        food_pk = self.kwargs.get('food_pk')
        if food_pk:
            return Review.objects.filter(food_id=food_pk)
        return Review.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        food_id = self.kwargs.get('food_pk')
        serializer.save(user=self.request.user, food_id=food_id)
