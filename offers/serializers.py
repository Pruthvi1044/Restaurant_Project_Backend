from rest_framework import serializers
from .models import Offer
from menu.serializers import DishSerializer


class OfferSerializer(serializers.ModelSerializer):
    dish = DishSerializer(read_only=True)

    class Meta:
        model = Offer
        fields = '__all__'
