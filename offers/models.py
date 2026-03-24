from django.db import models
from menu.models import Dish


class Offer(models.Model):
    title = models.CharField(max_length=200)
    discount_percent = models.PositiveIntegerField()
    dish = models.ForeignKey(
        Dish,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='offers'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.discount_percent}% off"
