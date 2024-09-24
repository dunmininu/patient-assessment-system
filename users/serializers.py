import re
from rest_framework import serializers

from users.choices import UserRole
from users.models import Tenant, User


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password_two = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, data):
        if data["password"] != data["password_two"]:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        validated_data.pop("password_two")
        user = User.objects.create_user(**validated_data, role=UserRole.ADMIN)
        user.set_password(validated_data["password"])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        )


class InviteUserSerializer(serializers.Serializer):
    email = serializers.EmailField()


class AcceptInviteSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_password(self, value):
        """
        Ensure the password meets the basic security requirements:
        - At least one digit
        - At least one uppercase letter
        - At least one special character
        """
        if not re.search(r"\d", value):
            raise serializers.ValidationError(
                "Password must contain at least one digit."
            )
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )
        if not re.search(r"[@$!%*?&]", value):
            raise serializers.ValidationError(
                "Password must contain at least one special character (@, $, !, %, *, ?, &)."
            )

        return value

    def save(self, user: User):
        try:
            # Update user information from validated data
            self._update_user_fields(user)

            # Create a new tenant for the user
            tenant = self._create_tenant(self.validated_data["username"])

            user.tenant = tenant
            user.is_active = True
            user.save()

            return user
        except Exception as e:
            raise serializers.ValidationError(
                f"An error occurred while saving the user: {str(e)}"
            )

    def _update_user_fields(self, user: User):
        user.username = self.validated_data["username"]
        user.first_name = self.validated_data["first_name"]
        user.last_name = self.validated_data["last_name"]
        user.set_password(self.validated_data["password"])

    def _create_tenant(self, username: str) -> Tenant:
        return Tenant.objects.create(name=username)
