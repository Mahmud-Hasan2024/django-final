# from django.contrib.auth import get_user_model
# from rest_framework.viewsets import ViewSet
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from users.serializers import RegisterSerializer, VerifyEmailSerializer, UserSerializer
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from users.tokens import email_verification_token
# from users.emails import send_verification_email

# User = get_user_model()

# class AuthViewSet(ViewSet):
#     permission_classes = [permissions.AllowAny]

#     @action(methods=['post'], detail=False, url_path='register')
#     def register(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()

#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         token = email_verification_token.make_token(user)
#         send_verification_email(user.email, uid, token)

#         return Response({"detail": "Registration successful. Check your email to verify."}, status=status.HTTP_201_CREATED)

#     @action(methods=['post'], detail=False, url_path='verify-email')
#     def verify_email(self, request):
#         serializer = VerifyEmailSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         user.is_active = True
#         user.is_email_verified = True
#         user.save()
#         return Response({"detail": "Email verified successfully."})

#     @action(methods=['get'], detail=False, permission_classes=[permissions.IsAuthenticated])
#     def me(self, request):
#         return Response(UserSerializer(request.user).data)
