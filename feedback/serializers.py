from rest_framework import serializers
from .models import Feedback




class FeedbackSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ['user']