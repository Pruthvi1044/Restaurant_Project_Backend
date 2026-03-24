from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from .models import Feedback
from .serializers import FeedbackSerializer

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


class CreateFeedbackView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = FeedbackSerializer(data=request.data)

        if serializer.is_valid():

            feedback = serializer.save(user=request.user)

            # send thank you email
            subject = "Thank You For Your Feedback"
            html_content = render_to_string('feedback/thank_you_email.html', {
                'feedback': feedback,
            })
            text_content = strip_tags(html_content)

            msg = EmailMultiAlternatives(
                subject,
                text_content,
                settings.DEFAULT_FROM_EMAIL,
                [feedback.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=False)

            return Response({
                "message": "Feedback submitted successfully"
            })

        return Response(serializer.errors)

    

class FeedbackListView(generics.ListAPIView):
    queryset = Feedback.objects.all().order_by('-created_at')
    serializer_class = FeedbackSerializer

