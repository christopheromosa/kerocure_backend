from rest_framework import serializers
from .models import LabTestSale

class LabTestSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTestSale
        fields = ['service', 'operation_count', 'total_amount', 'date']
