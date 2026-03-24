from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from urllib3 import request  # type: ignore
import logging

logger = logging.getLogger(__name__)

import booking

from .models import TableBooking
from .serializers import TableBookingSerializer

from rest_framework.permissions import IsAdminUser

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator




# class CreateBookingView(APIView):

#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         serializer = TableBookingSerializer(data=request.data)

#         if serializer.is_valid():

#             booking = serializer.save(user=request.user)

#             # email to admin
#             send_mail(
#                 "New Table Booking Request",
#                 f"""
#                     New table booking request received.

#                     Customer: {booking.name}
#                     Email: {booking.email}
#                     Guests: {booking.guests}
#                     Date: {booking.booking_date}
#                     Time: {booking.booking_time}

#                     Please review the booking in the admin panel.
#                     """,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [settings.EMAIL_HOST_USER],  # admin email
#                 fail_silently=False,
#             )

#             return Response({
#                 "message": "Table booking request sent"
#             })

#         return Response(serializer.errors)





@method_decorator(csrf_exempt, name='dispatch')
class CreateBookingView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = TableBookingSerializer(data=request.data)

        if serializer.is_valid():
            try:
                booking = serializer.save(user=request.user)
                print(f"Booking saved successfully: {booking.id}")
            except Exception as e:
                print(f"Error saving booking: {str(e)}")
                return Response({"error": "Error saving booking", "details": str(e)}, status=500)

            # create approve / reject links AFTER booking is created
            approve_link = f"https://pruthviraj.pythonanywhere.com/api/booking/approve/{booking.id}/"
            reject_link = f"https://pruthviraj.pythonanywhere.com/api/booking/reject/{booking.id}/"

            # email to admin
            try:
                send_mail(
                    "New Table Booking Request",
                    f"""
    New table booking request received.

    Customer: {booking.name}
    Email: {booking.email}
    Guests: {booking.guests}
    Date: {booking.booking_date}
    Time: {booking.booking_time}

    Approve Booking:
    {approve_link}

    Reject Booking:
    {reject_link}

    """,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                print("Admin email sent successfully")
            except Exception as e:
                print(f"Error sending admin email: {str(e)}")

            # --- SEND EMAIL TO CUSTOMER ---
            try:
                subject_customer = "Thank You for Your Booking at Swaad Indian Bistro"
                html_content_customer = render_to_string('booking/booking_confirmation_email.html', {
                    'booking': booking,
                })
                text_content_customer = strip_tags(html_content_customer)

                msg_customer = EmailMultiAlternatives(
                    subject_customer,
                    text_content_customer,
                    settings.DEFAULT_FROM_EMAIL,
                    [booking.email]
                )
                msg_customer.attach_alternative(html_content_customer, "text/html")
                msg_customer.send(fail_silently=False)
                print("Customer email sent successfully")
            except Exception as e:
                print(f"Error sending customer email: {str(e)}")
            # ------------------------------

            return Response({
                "message": "Table booking request sent",
                "booking_id": booking.id
            })

        print(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=400)

class MyBookingsView(generics.ListAPIView):

    serializer_class = TableBookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TableBooking.objects.filter(user=self.request.user)
    




# from rest_framework.permissions import IsAdminUser 
# Import the IsAdminUser permission class

class UpdateBookingStatusView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self, request, booking_id):

        try:
            booking = TableBooking.objects.get(id=booking_id)
        except TableBooking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)

        status = request.data.get("status")

        booking.status = status
        booking.save()

        return Response({
            "message": "Booking status updated",
            "status": booking.status
        })
    



class ApproveBookingView(APIView):

    def get(self, request, booking_id):

        booking = get_object_or_404(TableBooking, id=booking_id)

        booking.status = "approved"
        booking.save()

        # email to customer
        send_mail(
            "Your Table Booking is Confirmed",
            f"""
Hello {booking.name},

Your table booking has been CONFIRMED.

Booking Details:

Date: {booking.booking_date}
Time: {booking.booking_time}
Guests: {booking.guests}

We look forward to serving you.

Restaurant Team
""",
            settings.DEFAULT_FROM_EMAIL,
            [booking.email],
            fail_silently=False,
        )

        return Response({
            "message": "Booking approved and email sent to customer"
        })
    
    
class RejectBookingView(APIView):

    def get(self, request, booking_id):

        booking = get_object_or_404(TableBooking, id=booking_id)

        booking.status = "rejected"
        booking.save()

        # email to customer
        send_mail(
            "Table Booking Request Update",
            f"""
Hello {booking.name},

Unfortunately, your table booking request could not be confirmed.

Requested Date: {booking.booking_date}
Requested Time: {booking.booking_time}

This may be due to limited table availability.

Please try booking another time slot.

Thank you for understanding.

Restaurant Team
""",
            settings.DEFAULT_FROM_EMAIL,
            [booking.email],
            fail_silently=False,
        )

        return Response({
            "message": "Booking rejected and email sent to customer"
        })


class AdminBookingListView(generics.ListAPIView):
    """All bookings for admin — newest first."""
    from .serializers import TableBookingSerializer as _TBS
    serializer_class = _TBS
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return TableBooking.objects.all().order_by("-created_at")