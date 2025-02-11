from rest_framework import serializers
from .models import Triage


class TriageSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    staff_name = serializers.SerializerMethodField()

    class Meta:
        model = Triage
        fields = [
            "triage_id",
            "visit",
            "patient_name",
            "vital_signs",
            "staff_name",
            "recorded_at",
        ]

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
            f"{obj.recorded_by.first_name} {obj.recorded_by.last_name}"
            if obj.recorded_by
            else None
        )
