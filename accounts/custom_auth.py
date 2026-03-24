from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):

        data = super().validate(attrs)

        if not self.user.is_verified:
            raise serializers.ValidationError(
                "Please verify your email before logging in."
            )

        data['username'] = self.user.username
        data['is_staff'] = self.user.is_staff

        return data