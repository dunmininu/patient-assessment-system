import re
from rest_framework import serializers

from users.choices import UserRole
from users.models import User


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
        return User.objects.create_user(**validated_data, role=UserRole.ADMIN)


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
        user.set_password(self.validated_data["password"])
        user.is_active = True
        user.save()
        return user
