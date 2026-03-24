from django.urls import path
from .views import (
    AdminBookingListView,
    ApproveBookingView,
    CreateBookingView,
    MyBookingsView,
    RejectBookingView,
    UpdateBookingStatusView
)

urlpatterns = [

    path('create/', CreateBookingView.as_view()),
    path('my-bookings/', MyBookingsView.as_view()),
    path('update-status/<int:booking_id>/', UpdateBookingStatusView.as_view()),
    path('approve/<int:booking_id>/', ApproveBookingView.as_view()),
    path('reject/<int:booking_id>/', RejectBookingView.as_view()),
    path('admin/all/', AdminBookingListView.as_view()),
]
