from rest_framework import serializers
from .models import PhysicianNote


class ConsultationSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    staff_name = serializers.SerializerMethodField()

    class Meta:
        model = PhysicianNote
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
            f"{obj.physician.first_name} {obj.physician.last_name}"
            if obj.physician
            else None
        )
