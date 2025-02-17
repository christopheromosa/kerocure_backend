from rest_framework import serializers
from .models import Billing


class BillingSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    staff_name = serializers.SerializerMethodField()
    class Meta:
        model = Billing
        fields = "__all__"
        extra_fields = ["patient_name", "staff_name"]

    def get_patient_name(self, obj):
        """Fetch the patient's full name from the related Visit model."""
        return (
            f"{obj.visit.patient.first_name} {obj.visit.patient.last_name}"
            if obj.visit and obj.visit.patient
            else None
        )

    def get_staff_name(self, obj):
        """Fetch the staff's full name from the recorded_by field."""
        return (
            f"{obj.billed_by.first_name} {obj.billed_by.last_name}"
            if obj.billed_by
            else None
        )
