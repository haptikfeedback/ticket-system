from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    at_risk = serializers.BooleanField(read_only=True)

    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "tenant")
