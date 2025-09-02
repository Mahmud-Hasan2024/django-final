from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
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
        qs = Review.objects.select_related('user')
        if food_pk:
            return qs.filter(food_id=food_pk)
        return qs

    def perform_create(self, serializer):
        food_id = self.kwargs.get('food_pk')
        if not food_id:
            raise ValidationError("Food ID is required.")

        try:
            serializer.save(user=self.request.user, food_id=food_id)
        except IntegrityError:
            raise ValidationError(
                {"detail": "You have already reviewed this product. Please update your review instead."}
            )
