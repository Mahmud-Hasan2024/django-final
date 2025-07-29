from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from users.tokens import email_verification_token

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data, is_active=False)
        return user

class VerifyEmailSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        uid = attrs.get('uid')
        token = attrs.get('token')
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except Exception:
            raise serializers.ValidationError("Invalid uid.")

        if not email_verification_token.check_token(user, token):
            raise serializers.ValidationError("Invalid or expired token.")

        attrs['user'] = user
        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_email_verified']
