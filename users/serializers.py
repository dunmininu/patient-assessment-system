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
