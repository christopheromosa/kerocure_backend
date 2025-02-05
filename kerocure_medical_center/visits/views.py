from django.shortcuts import render
from .models import Visit
from rest_framework.viewsets import ModelViewSet
from .serializers import VisitSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from patients.serializers import PatientSerializer
from rest_framework import status
from django.utils import timezone
from triage.models import Triage
from consultation.models import PhysicianNote
from patients.models import Patient
from lab.models import LabResult
from pharmacy.models import Medication


# Create your views here.
class VisitViewSet(ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer

    def create(self, request, *args, **kwargs):
        """
        Prevent duplicate visits for the same patient on the same day.
        """
        patient_id = request.data.get("patient")
        today = timezone.now().date()

        # Check if the patient already has a visit today
        existing_visit = Visit.objects.filter(
            patient_id=patient_id, visit_date=today
        ).first()
        if existing_visit:
            return Response(
                {"detail": "Visit already exists for today."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().create(request, *args, **kwargs)


@api_view(["GET"])
def triage_patients(request):
    """
    Fetch patients whose visit's current_state is 'triage' and next_state is 'consultation'.
    """
    visits = Visit.objects.filter(
        current_state="TRIAGE", next_state="CONSULTATION"
    ).select_related("patient")
    patients = [visit.patient for visit in visits]
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def consultation_patients(request):
    """
    Fetch patients whose visit's current_state is 'consultation' and next_state is 'lab'.
    """
    visits = Visit.objects.filter(
        current_state="CONSULTATION", next_state="LABORATORY"
    ).select_related("patient")
    patients = [visit.patient for visit in visits]
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def lab_patients(request):
    """
    Fetch patients whose visit's current_state is 'lab' and next_state is 'consultation'.
    """
    visits = Visit.objects.filter(
        current_state="LABORATORY", next_state="CONSULTATION"
    ).select_related("patient")
    patients = [visit.patient for visit in visits]
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def pharmacy_patients(request):
    """
    Fetch patients whose visit's current_state is 'consultation' and next_state is 'lab'.
    """
    visits = Visit.objects.filter(
        current_state="CONSULTATION", next_state="PHARMACY"
    ).select_related("patient")
    patients = [visit.patient for visit in visits]
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def billing_patients(request):
    """
    Fetch patients whose visit's current_state is 'pharmacy' and next_state is 'billing'.
    """
    visits = Visit.objects.filter(
        current_state="PHARMACY", next_state="BILLING"
    ).select_related("patient")
    patients = [visit.patient for visit in visits]
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def admin_patients(request):
    """
    Fetch patients whose visit's current_state is 'pharmacy' and next_state is 'billing'.
    """
    visits = Visit.objects.filter(
        current_state="BILLING", next_state="COMPLETED"
    ).select_related("patient")
    patients = [visit.patient for visit in visits]
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_today_visit(request, patientId):
    today = timezone.now().date()
    print(today)
    visit = Visit.objects.filter(patient_id=patientId, visit_date=today).first()
    print(visit.visit_date)
    if not visit:
        return Response({"error": "No visit found for today"}, status=404)
    triage = Triage.objects.filter(visit=visit).first()
    consultation = PhysicianNote.objects.filter(visit=visit).first()
    patient = Patient.objects.filter(id=patientId).first()
    lab = LabResult.objects.filter(visit=visit).first()
    medication = Medication.objects.filter(visit=visit).first()
    return Response(
        {
            "visit_id": visit.visit_id,
            "triage_data": (
                {
                    "triage_id": triage.triage_id,
                    "vital_signs": triage.vital_signs,
                    "recorded_by": (
                        triage.recorded_by.id if triage.recorded_by else None
                    ),
                    "recorded_at": triage.recorded_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
                if triage
                else None
            ),
            "consultation_data": (
                {
                    "note_id": consultation.note_id,
                    "diagnosis": consultation.diagnosis,
                    "prescription": consultation.prescription,
                    "lab_test_ordered": consultation.lab_tests_ordered,
                    "physician": (
                        consultation.physician.id if consultation.physician else None
                    ),
                    "recorded_at": consultation.recorded_at,
                }
                if consultation
                else None
            ),
            "patient_data": (
                {
                    "patient_id": patient.pk,
                    "first_name": patient.first_name,
                    "last_name": patient.last_name,
                    "dob": patient.dob,
                    "contact_number": patient.contact_number,
                }
                if patient
                else None
            ),
            "lab_data": (
                {
                    "result_id": lab.result_id,
                    "results": lab.result,
                    "test_name": lab.test_name,
                }
                if lab
                else None
            ),
            "pharmacy_data": (
                {
                    "medication_id": medication.medication_id,
                    "cost": medication.cost,
                }
                if medication else None
            ),
        }
    )
