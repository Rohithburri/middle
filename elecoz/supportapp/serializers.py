from rest_framework import serializers
from .models import SupportTicket

class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = '__all__'