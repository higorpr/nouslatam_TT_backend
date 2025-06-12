from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, permissions, response, status
from drf_spectacular.utils import extend_schema

from .serializers import (
    PasswordChangeSerializer,
    PasswordResetRequestSerializer,
    UserCreateSerializer,
    UserDetailSerializer,
    PasswordResetConfirmSerializer
)


class UserCreateView(generics.CreateAPIView):
    """
    View for creating a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for getting, updating and deleting logged in users.
    """
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Overrides the default get_object method to return the user making
        the request.
        """
        return self.request.user


class PasswordChangeView(generics.GenericAPIView):
    """
    View for changing a user's password.
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Overrides the default get_object method to return the user making
        the request.
        """
        return self.request.user

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests for changing a user's password.
        """
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return response.Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)


class PasswordResetRequestView(generics.GenericAPIView):
    """
    View for requesting a password reset for logged off users.
    """
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *arg, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.get(email__iexact=email)

        # Generate token and uid for password change
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Build reset link
        reset_link = f"{settings.FRONTEND_DOMAIN}/password-reset-confirm/{uid}/{token}"
        print(settings.FRONTEND_DOMAIN)

        # Message Body
        email_body = f"""
        Hello {user.first_name} {user.last_name},
        
        You have requested to reset your password. 
        Please click the link below to reset your password:\n
        {reset_link}
        
        If you did not request this, please ignore this email.
        
        Best Regards,
        Task Manager Team
        """

        # Send Email
        send_mail(
            subject='Password Reset Request',
            message=email_body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        # Always return the same response to avoid hackers getting registered emails
        return response.Response({
            "detail":
            "Password reset link has been sent to the user's email"
        },
            status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    """
    View for confirming a password reset for logged off users.
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *arg, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({
            "detail": "Password has been successfully reset"
        }, status=status.HTTP_200_OK)
