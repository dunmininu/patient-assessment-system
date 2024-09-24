from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "full_name",
            "gender",
            "phone_number",
            "date_of_birth",
            "age",
            "address",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class PatientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "full_name",
            "gender",
            "phone_number",
            "date_of_birth",
            "age",
            "address",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        tenant = getattr(user, "tenant", None)

        if tenant is None:
            raise serializers.ValidationError("User must be associated with a tenant.")

        validated_data["tenant"] = tenant
        return super().create(validated_data)
