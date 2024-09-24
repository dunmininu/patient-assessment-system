from django.db import models
from django.utils import timezone

from users.models import Tenant


class Patient(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="tenant_patients"
    )

    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    age = models.PositiveIntegerField()
    address = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
