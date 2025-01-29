from rest_framework import serializers
from .models import Medication

class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = "__all__"
