# serializers.py
from rest_framework import serializers
from wagers.models import Wager, WagerRequest, Participant

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'

class WagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wager
        fields = '__all__'

class WagerRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WagerRequest
        fields = '__all__'