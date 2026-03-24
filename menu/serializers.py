from rest_framework import serializers
from .models import Category, Dish


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class DishSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = '__all__'

    def get_discounted_price(self, obj):
        return obj.get_discounted_price()