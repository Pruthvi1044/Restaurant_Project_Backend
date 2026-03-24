from rest_framework import generics, status
from .models import User
from .serializers import RegisterSerializer, UserProfileSerializer, ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse
from .tokens import email_verification_token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework_simplejwt.views import TokenObtainPairView

from .custom_auth import CustomTokenObtainPairSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_decode
from .tokens import email_verification_token




class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):

        user = serializer.save()
        
        # Automatically verify user
        user.is_verified = True
        user.save()

        subject = "Welcome to Swaad Indian Bistro!"
        html_content = render_to_string('accounts/welcome_email.html', {
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

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer




# Create Email Verification API 
class VerifyEmailView(APIView):

    def get(self, request, uid, token):

        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id)

            if email_verification_token.check_token(user, token):

                user.is_verified = True
                user.save()

                return Response({"message": "Email verified successfully"})

            return Response({"error": "Invalid verification link"})

        except:
            return Response({"error": "Invalid verification link"})


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)