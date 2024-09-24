from django.core import signing
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.choices import UserRole
from users.serializers import (
    AcceptInviteSerializer,
    CreateUserSerializer,
    InviteUserSerializer,
)

from rest_framework.permissions import IsAuthenticated, AllowAny

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
        serializer = InviteUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        role = UserRole.CLINICIAN

        if User.objects.filter(username=email).exists():
            return Response(
                {"detail": "User with this email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create(
            username=email,
            email=email,
            role=role,
            is_active=False,
        )

        token = signing.dumps(
            {
                "user_id": user.id,
                "token": get_random_string(32),
            }
        )

        invite_link = f"{settings.FRONTEND_URL}/accept-invite/{token}"

        subject = "Clinician Invitation to Join Kochanet"
        message = f"You have been invited to join Kochanet as a clinician. Click the following link to complete your registration: {invite_link}"
        from_email = settings.DEFAULT_FROM_EMAIL

        send_mail(
            subject,
            message,
            from_email,
            [email],
            fail_silently=False,
        )

        return Response({"message": "Invitation sent."}, status=200)

    @action(detail=False, methods=["post"], url_path="accept-invite/(?P<token>[^/.]+)")
    def accept_invite(self, request, token):
        """
        Accept an invitation by validating the token,
        setting the user's password, and activating the account.
        """
        try:
            data = signing.loads(token)
            user_id = data.get("user_id")
            user = User.objects.get(id=user_id, is_active=False)
        except (User.DoesNotExist, signing.BadSignature):
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = AcceptInviteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=user)
            return Response(
                {"message": "Account activated successfully."},
                status=status.HTTP_200_OK,
            )

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
