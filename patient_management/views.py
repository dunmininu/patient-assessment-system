from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from users.permissions import IsAdmin, IsTenantUser

from .models import Patient
from .serializers import PatientCreateSerializer, PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing patient instances.
    """

    queryset = Patient.objects.all()
    permission_classes = [IsTenantUser | IsAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        "gender",
        "full_name",
        "date_of_birth",
    ]
    ordering_fields = ["full_name", "date_of_birth", "created_at"]
    ordering = ["full_name"]

    def get_serializer_class(self):
        if self.action == "create":
            return PatientCreateSerializer
        return PatientSerializer
