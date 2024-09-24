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
