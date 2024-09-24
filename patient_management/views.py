from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from .models import Patient
from .serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing patient instances.
    """

    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        "gender",
        "full_name",
        "date_of_birth",
    ]
    ordering_fields = ["full_name", "date_of_birth", "created_at"]
    ordering = ["full_name"]

    def perform_create(self, serializer):
        """
        Override this method if you need to customize how the instance is saved.
        """
        serializer.save()
