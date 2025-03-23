from rest_framework import serializers
from .models import LabTestSale
from django.utils import timezone

class LabTestSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTestSale
        fields = ['service', 'operation_count', 'total_amount', 'date']
          

    def validate_operation_count(self, value):
        """Ensure operation_count is a non-negative integer."""
        if value < 0:
            raise serializers.ValidationError("operation_count must be a non-negative integer.")
        return value

    def validate_total_amount(self, value):
        """Ensure total_amount is a non-negative decimal."""
        if value < 0:
            raise serializers.ValidationError("total_amount must be a non-negative decimal.")
        return value

    def validate_date(self, value):
        """Ensure date is in the correct format and not in the future."""
        if value > timezone.now().date():
            raise serializers.ValidationError("date cannot be in the future.")
        return value
