from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Dish(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="dishes"
    )

    name = models.CharField(max_length=200)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to="dishes/"
    )

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def get_discounted_price(self):
        """Returns the price after applying active offers."""
        active_offer = self.offers.filter(is_active=True).first()
        if active_offer:
            discount_amount = (self.price * active_offer.discount_percent) / 100
            return self.price - discount_amount
        return self.price

    def __str__(self):
        return self.name