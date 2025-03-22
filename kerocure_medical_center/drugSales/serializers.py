from .models import DrugSale
from rest_framework import serializers

class DrugSaleSerializer(serializers.ModelSerializer):
    drug_name = serializers.CharField(source='drug.drug_name', read_only=True)
    class Meta:
        model = DrugSale
        fields = ['id', 'drug','drug_name', 'quantity_sold', 'total_amount', 'date']

    def validate_quantity_sold(self, value):
            # Access the drug object from the context
            drug = self.context.get('drug')
            if not drug:
                raise serializers.ValidationError("Drug context is missing.")
    
            # Add your custom validation logic here
            if value < 0:
                raise serializers.ValidationError("Quantity sold cannot be negative.")
            return value

