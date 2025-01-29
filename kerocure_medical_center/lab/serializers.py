from rest_framework import serializers
from .models import LabResult


class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResult
        fields = "__all__"
