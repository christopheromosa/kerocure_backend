from rest_framework import serializers
from .models import Drug


class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = "__all__"
    def update(self, instance, validated_data):
            instance.drug_name = validated_data.get('drug_name', instance.drug_name)
            instance.cost = validated_data.get('cost', instance.cost)
            instance.quantity = validated_data.get('quantity', instance.quantity)
            
            # Save the instance to update the quantity
            instance.save()
            
            # Update the status based on the new quantity
            instance.update_status()
            
            return instance
