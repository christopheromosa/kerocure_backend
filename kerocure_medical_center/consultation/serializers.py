from rest_framework import serializers
from .models import PhysicianNote


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicianNote
        fields = "__all__"
