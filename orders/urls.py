from django.urls import path
from .views import AddToCartView, AdminDashboardView, AdminOrderListView, CancelOrderView, CartView, CreateOrderView, MyOrdersView, OrderDetailView, OrderHistoryView, RemoveFromCartView, UpdateOrderStatusView


urlpatterns = [

    path('add/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('my-cart/', CartView.as_view(), name='my-cart'),
    path('create-order/', CreateOrderView.as_view(), name='create-order'),
    path('my-orders/', MyOrdersView.as_view(), name='my-orders'),
    path('update-status/<int:order_id>/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    path("admin-dashboard/", AdminDashboardView.as_view(), name='admin-dashboard'),
    path("admin/all/", AdminOrderListView.as_view(), name='admin-orders-list'),
    path("order-detail/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path('cancel-order/<int:order_id>/', CancelOrderView.as_view(), name='cancel-order'),

]

