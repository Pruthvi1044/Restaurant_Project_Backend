from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart, CartItem, Order, OrderItem, Cart
from menu.models import Dish
from .serializers import CartSerializer, OrderSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes

from rest_framework import generics


from django.db.models import Sum
from accounts.models import User
from booking.models import TableBooking

from rest_framework.generics import ListAPIView, RetrieveAPIView

from django.shortcuts import get_object_or_404


User = get_user_model()

# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])

class AddToCartView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user
        dish_id = request.data.get("dish_id")
        quantity = int(request.data.get("quantity", 1))

        dish = Dish.objects.get(id=dish_id)

        cart, _ = Cart.objects.get_or_create(user=user)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            dish=dish
        )

        if created:
            # Newly created item — set quantity directly (model default is 1 already)
            item.quantity = quantity if quantity > 0 else 1
        else:
            # Existing item — adjust by delta
            item.quantity += quantity
            if item.quantity <= 0:
                item.delete()
                return Response({"message": "Item removed from cart"})

        item.save()

        return Response({"message": "Item added to cart"})


class RemoveFromCartView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        dish_id = request.data.get("dish_id")

        try:
            cart = Cart.objects.get(user=user)
            item = CartItem.objects.get(cart=cart, dish_id=dish_id)
            item.delete()
            return Response({"message": "Item removed from cart"})
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response({"error": "Item not found in cart"}, status=404)
    

class CartView(generics.RetrieveAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = CartSerializer

    def get_object(self):

        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)

        return cart


class OrderDetailView(RetrieveAPIView):

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

        

class CreateOrderView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user
        payment_method = request.data.get("payment_method", "cash")
        shipping_address = request.data.get("shipping_address")

        if shipping_address and not user.address:
            user.address = shipping_address
            user.save()

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart is empty"},
                status=400
            )

        cart_items = cart.items.all()

        if not cart_items:
            return Response(
                {"error": "Cart has no items"},
                status=400
            )

        total = 0

        for item in cart_items:
            # Use discounted price if applicable
            price = item.dish.get_discounted_price()
            total += price * item.quantity

        order = Order.objects.create(
            user=user,
            total_amount=total,
            payment_method=payment_method,
            shipping_address=shipping_address
        )

        for item in cart_items:
            price = item.dish.get_discounted_price()
            OrderItem.objects.create(
                order=order,
                dish=item.dish,
                quantity=item.quantity,
                price=price
            )

        # Send Order Confirmation Email
        try:
            subject = f"Order Confirmation - {order.order_number}"
            html_content = render_to_string('orders/order_confirmation_email.html', {
                'order': order,
                'user': user,
            })
            text_content = strip_tags(html_content)

            msg = EmailMultiAlternatives(
                subject,
                text_content,
                settings.DEFAULT_FROM_EMAIL,
                [user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=False)
        except Exception as e:
            print(f"Error sending order confirmation email: {e}")

        cart_items.delete()

        return Response({
            "message": "Order created successfully",
            "order_id": order.id,
            "order_number": order.order_number,
        })


class AdminOrderListView(generics.ListAPIView):
    """All orders for admin — newest first, with items."""
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Order.objects.all().order_by("-created_at")

class MyOrdersView(generics.ListAPIView):

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")





class UpdateOrderStatusView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self, request, order_id):

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        new_status = request.data.get("status")

        order.status = new_status
        order.save()

        return Response({
            "message": "Order status updated",
            "order_id": order.id,
            "status": order.status
        })


class AdminDashboardView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        total_orders = Order.objects.count()

        total_revenue = Order.objects.filter(
            payment_status="paid"
        ).aggregate(Sum("total_amount"))["total_amount__sum"] or 0

        total_customers = User.objects.filter(role="customer").count()

        total_bookings = TableBooking.objects.count()

        menu_items = Dish.objects.count()

        pending_orders = Order.objects.filter(status="pending").count()

        return Response({
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "total_customers": total_customers,
            "total_bookings": total_bookings,
            "menu_items": menu_items,
            "pending_orders": pending_orders
        })


class OrderHistoryView(ListAPIView):

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Order.objects.filter(
            user=self.request.user
        ).order_by("-created_at")






class CancelOrderView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):

        order = get_object_or_404(
            Order,
            id=order_id,
            user=request.user
        )

        if order.status != "pending":
            return Response({
                "error": "Order cannot be cancelled after preparation has started."
            })

        order.status = "cancelled"
        order.save()

        return Response({
            "message": "Order cancelled successfully."
        })