from rest_framework import serializers
from reviews.models import Review
from django.contrib.auth import get_user_model

User = get_user_model()

class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='get_full_name')

    class Meta:
        model = User
        fields = ['id', 'name']



class ReviewSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']