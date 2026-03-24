from rest_framework import serializers
from .models import TableBooking


class TableBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = TableBooking
        fields = '__all__'
        read_only_fields = ['user']