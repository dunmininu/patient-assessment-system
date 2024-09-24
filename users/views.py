
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.serializers import (
    CreateUserSerializer,
)

from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

from users.serializers import UserSerializer
from users.permissions import IsAdmin

User = get_user_model()


# Create your views here.
class AuthenticationViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()
    authentication_classes = []
    permission_classes = [AllowAny]


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Override permissions so that only admins can invite users.
        """
        if self.action == "invite_user":
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(
        detail=False,
        methods=["post"],
        url_path="invite",
        permission_classes=[IsAuthenticated, IsAdmin],
    )
    def invite_user(self, request):
        """
        Invite a clinician by sending an email.
        Only Admin users can perform this action.
        """
        email = request.data.get("email")
        if not email:
            return Response(
                {"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        role = "Clinician"  # For invitation, we'll assume it's always for Clinicians.

        # Check if the user already exists
        if User.objects.filter(username=email).exists():
            return Response(
                {"detail": "User with this email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create an inactive user account
        User.objects.create(
            username=email,
            email=email,
            role=role,
            is_active=False,
        )

        invite_link = f"{settings.FRONTEND_URL}/invite/accept?email={email}"
        subject = "You're Invited to Kochanet!"
        message = f"Hello,\n\nYou've been invited to join Kochanet as a Clinician. Click the link below to accept the invitation and set up your account:\n\n{invite_link}\n\nBest regards,\nKochanet Team"
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return Response(
            {"detail": f"Invitation sent to {email}."}, status=status.HTTP_200_OK
        )
