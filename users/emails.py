from django.conf import settings
from django.core.mail import send_mail

def send_verification_email(email, uid, token):
    verify_url = f"{settings.FRONTEND_URL}/verify-email?uid={uid}&token={token}"
    send_mail(
        subject="Verify your account",
        message=f"Click the link to verify: {verify_url}",
        from_email="no-reply@example.com",
        recipient_list=[email],
    )
