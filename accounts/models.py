from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    )

    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username