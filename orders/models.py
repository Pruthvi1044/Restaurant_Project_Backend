from django.db import models
from django.conf import settings
from menu.models import Dish


User = settings.AUTH_USER_MODEL


import uuid



class Cart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class CartItem(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.dish.name


# class Order(models.Model):

#     STATUS_CHOICES = (
#         ('pending', 'Pending'),
#         ('preparing', 'Preparing'),
#         ('ready', 'Ready'),
#         ('delivered', 'Delivered'),
#         ('cancelled', 'Cancelled'),
#     )

#     user = models.ForeignKey(User, on_delete=models.CASCADE)

#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)

#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default='pending'
#     )

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order {self.id}"



def generate_order_number():
    return f"REST-{uuid.uuid4().hex[:8].upper()}"

class Order(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    PAYMENT_METHOD = (
        ('online', 'Online'),
        ('cash', 'Cash'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    order_number = models.CharField(
        max_length=30,
        unique=True,
        default=generate_order_number
    )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS,
        default='pending'
    )

    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD,
        default='online'
    )
    
    shipping_address = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_number
    


# class OrderItem(models.Model):

#     order = models.ForeignKey(
#         Order,
#         on_delete=models.CASCADE,
#         related_name="items"
#     )

#     dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

#     quantity = models.PositiveIntegerField()

#     price = models.DecimalField(max_digits=8, decimal_places=2)

#     def __str__(self):
#         return self.dish.name


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(max_digits=8, decimal_places=2)

    def get_total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return self.dish.name