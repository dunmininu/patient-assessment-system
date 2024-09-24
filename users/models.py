from django.db import models
from django.contrib.auth.models import AbstractUser

from users.choices import UserRole


# Create your models here.
class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.ADMIN,
    )
    mobile = models.CharField(max_length=20, null=True, blank=True)
