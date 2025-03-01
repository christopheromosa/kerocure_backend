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
        # today = timezone.now().date()

        # Check if the patient already has a visit today
        existing_visit = Visit.objects.filter(
            patient_id=patient_id,
            # visit_date=today
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
    today = timezone.now().date()
    visits = Visit.objects.filter(
        current_state="TRIAGE",
        next_state="CONSULTATION",
        # visit_date=today
    ).select_related("patient", "department")
    patients_data = []
    for visit in visits:
        patient_data = PatientSerializer(visit.patient).data  # Serialize patient
        patient_data["department"] = {
            "id": visit.department.id if visit.department else None,
            "name": visit.department.name if visit.department else "Unknown",
        }  # Add department info
        patients_data.append(patient_data)

    return Response(patients_data)


@api_view(["GET"])
def triage_patients_department(request, department_id):
    """
    Fetch patients whose visit's current_state is 'triage' and next_state is 'consultation and department specified'.
    """
    today = timezone.now().date()
    visits = Visit.objects.filter(
        current_state="TRIAGE",
        next_state="CONSULTATION",
        department=department_id,
        # visit_date=today
    ).select_related("patient")
    patients = [visit.patient for visit in visits]
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def consultation_patients(request):
    """
    Fetch patients whose visit's current_state is 'consultation' and next_state is 'lab'.
    """
    today = timezone.now().date()
    visits = Visit.objects.filter(
        current_state="CONSULTATION",
        next_state="LABORATORY",
        # visit_date=today
    ).select_related("patient")
    patients = [visit.patient for visit in visits]
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def lab_patients(request):
    """
    Fetch patients whose visit's current_state is 'lab' and next_state is 'consultation'.
    """
    today = timezone.now().date()
    visits = Visit.objects.filter(
        current_state="LABORATORY",
        next_state="CONSULTATION",
        # visit_date=today
    ).select_related("patient")
    patients = [visit.patient for visit in visits]
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def pharmacy_patients(request):
    """
    Fetch patients whose visit's current_state is 'consultation' and next_state is 'lab'.
    """
    today = timezone.now().date()
    visits = Visit.objects.filter(
        current_state="CONSULTATION", next_state="PHARMACY", visit_date=today
    ).select_related("patient")
    patients = [visit.patient for visit in visits]
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def billing_patients(request):
    """
    Fetch patients whose visit's current_state is 'pharmacy' and next_state is 'billing'.
    """
    today = timezone.now().date()
    visits = Visit.objects.filter(
        current_state="PHARMACY",
        next_state="BILLING",
        # visit_date=today
    ).select_related("patient")
    patients = [visit.patient for visit in visits]
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def admin_patients(request):
    """
    Fetch patients whose visit's current_state is 'pharmacy' and next_state is 'billing'.
    """
    today = timezone.now().date()
    visits = Visit.objects.filter(
        current_state="BILLING",
        next_state="COMPLETED",
        # visit_date=today
    ).select_related("patient")
    patients = [visit.patient for visit in visits]
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_today_visit(request, patientId):
    today = timezone.now().date()
    print(today)
    visit = Visit.objects.filter(
        patient_id=patientId,
        #  visit_date=today
    ).first()
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
                {"result": lab.result, "total_cost": lab.total_cost} if lab else None
            ),
            "pharmacy_data": (
                {
                    "medication_id": medication.medication_id,
                    "cost": medication.cost,
                }
                if medication
                else None
            ),
        }
    )


@api_view(["GET"])
def get_patient_history(request, patientId):
    patient = Patient.objects.prefetch_related(
        "visits__triage",
        "visits__consultation",
        "visits__lab",
        "visits__pharmacy",
        "visits__billing",
    ).get(patient_id=patientId)

    history = []

    for visit in patient.visits.all():
        visit_data = {
            "visit_id": visit.id,
            "visit_date": visit.visit_date,
            "triage": list(visit.triage.all().values()),
            "consultation": list(visit.consultation.all().values()),
            "lab": list(visit.lab.all().values()),
            "pharmacy": list(visit.pharmacy.all().values()),
            "billing": list(visit.billing.all().values()),
        }
        history.append(visit_data)

    return history


@api_view(["GET"])
def get_visit_details(visit_id):
    visit = Visit.objects.prefetch_related(
        "triage", "consultation", "lab", "pharmacy", "billing"
    ).get(id=visit_id)

    visit_data = {
        "visit_id": visit.id,
        "visit_date": visit.visit_date,
        "visit_type": visit.visit_type,
        "triage": list(visit.triage.all().values()),
        "consultation": list(visit.consultation.all().values()),
        "lab": list(visit.lab.all().values()),
        "pharmacy": list(visit.pharmacy.all().values()),
        "billing": list(visit.billing.all().values()),
    }

    return visit_data


@api_view(["GET"])
def get_all_visits(request):
    """
    Fetch all visits.
    """
    visits = Visit.objects.prefetch_related(
        "triage", "consultation", "lab", "pharmacy", "billing"
    ).all()

    visit_data = []
    for visit in visits:
        visit_data.append(
            {
                "id": visit.id,
                "visit_date": visit.visit_date,
                "visit_type": visit.visit_type,
                "patient_name": f"{visit.patient.first_name} {visit.patient.last_name}",
                "patient_id": visit.patient.id,
                "triage": list(visit.triage.all().values()),
                "consultation": list(visit.consultation.all().values()),
                "lab": list(visit.lab.all().values()),
                "pharmacy": list(visit.pharmacy.all().values()),
                "billing": list(visit.billing.all().values()),
            }
        )

    return Response(visit_data)


@api_view(["GET"])
def get_visits_by_patient_name(request, patient_name):
    """
    Fetch visits for a specific patient by name.
    """
    visits = Visit.objects.prefetch_related(
        "triage", "consultation", "lab", "pharmacy", "billing"
    ).filter(patient__first_name__icontains=patient_name) | Visit.objects.filter(
        patient__last_name__icontains=patient_name
    )

    visit_data = []
    for visit in visits:
        visit_data.append(
            {
                "id": visit.id,
                "visit_date": visit.visit_date,
                "visit_type": visit.visit_type,
                "patient_name": f"{visit.patient.first_name} {visit.patient.last_name}",
                "patient_id": visit.patient.id,
                "triage": list(visit.triage.all().values()),
                "consultation": list(visit.consultation.all().values()),
                "lab": list(visit.lab.all().values()),
                "pharmacy": list(visit.pharmacy.all().values()),
                "billing": list(visit.billing.all().values()),
            }
        )

    return Response(visit_data)
