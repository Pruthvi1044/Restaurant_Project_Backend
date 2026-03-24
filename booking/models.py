from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class TableBooking(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)

    email = models.EmailField()

    phone = models.CharField(max_length=15)

    booking_date = models.DateField()

    booking_time = models.TimeField()

    guests = models.PositiveIntegerField()

    message = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.name}"