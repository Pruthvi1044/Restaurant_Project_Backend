from rest_framework import generics
from .models import Offer
from .serializers import OfferSerializer


class OfferListView(generics.ListAPIView):
    queryset = Offer.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = OfferSerializer
