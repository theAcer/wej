# views.py
from rest_framework import generics
from ..models import Wager, WagerRequest, Participant
from .serializers import WagerSerializer, WagerRequestSerializer, ParticipantSerializer

class ParticipantList(generics.ListCreateAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

class ParticipantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

class WagerList(generics.ListCreateAPIView):
    queryset = Wager.objects.all()
    serializer_class = WagerSerializer

class WagerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wager.objects.all()
    serializer_class = WagerSerializer

class WagerRequestList(generics.ListCreateAPIView):
    queryset = WagerRequest.objects.all()
    serializer_class = WagerRequestSerializer

class WagerRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = WagerRequest.objects.all()
    serializer_class = WagerRequestSerializer