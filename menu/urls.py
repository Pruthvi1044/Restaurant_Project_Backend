from django.urls import path
from .views import CategoryListView, DishListView, DishDetailView, DishSearchView


urlpatterns = [

    path('categories/', CategoryListView.as_view()),
    path('dishes/', DishListView.as_view()),
    path('dishes/<int:pk>/', DishDetailView.as_view()),
    path('search/', DishSearchView.as_view()),

]