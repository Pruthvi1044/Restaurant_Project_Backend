from rest_framework import generics
from .models import Category, Dish
from .serializers import CategorySerializer, DishSerializer

from django.db.models import Q


# Get all categories
class CategoryListView(generics.ListAPIView):

    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


# Get all dishes
class DishListView(generics.ListAPIView):

    queryset = Dish.objects.filter(is_available=True)
    serializer_class = DishSerializer


# Dish detail
class DishDetailView(generics.RetrieveAPIView):

    queryset = Dish.objects.all()
    serializer_class = DishSerializer



class DishSearchView(generics.ListAPIView):

    serializer_class = DishSerializer

    def get_queryset(self):

        query = self.request.query_params.get('q')

        if query:
            return Dish.objects.filter(
                Q(name__icontains=query) |
                Q(category__name__icontains=query)
            )

        return Dish.objects.all()