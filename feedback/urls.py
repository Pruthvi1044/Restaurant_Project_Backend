from django.urls import path
from .views import CreateFeedbackView, FeedbackListView

urlpatterns = [

    path('create/', CreateFeedbackView.as_view()),

    path('all/', FeedbackListView.as_view()),

]