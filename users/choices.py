from django.db.models import TextChoices


class UserRole(TextChoices):
    CLINICIAN = "Clinician"
    ADMIN = "Admin"
