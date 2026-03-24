from django.urls import path
from .views import RegisterView, VerifyEmailView, CustomLoginView, ProfileView, ChangePasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('verify-email/<str:uid>/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]