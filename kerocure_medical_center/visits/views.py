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
from departments.models import Department
from departments.serializers import DepartmentSerializer


# Create your views here.
class VisitViewSet(ModelViewSet):
    queryset = Visit.objects.all().order_by("-visit_id")
    serializer_class = VisitSerializer

    def perform_create(self, serializer):
        """
        Automatically set visit_type:
        - 'Visit' if it's the first visit of the day
        - 'Revisit' if the patient already has a visit today
        """
        patient = serializer.validated_data["patient"]
        today = timezone.now().date()

         # Save the instance with the determined visit_type
        serializer.save()


@api_view(["GET"])
def triage_patients(request):
    """
    Fetch patients whose visit's current_state is 'triage' and next_state is 'consultation'.
    """
    today = timezone.now().date()
    visits = Visit.objects.filter(
        next_state="CONSULTATION",
        current_state__in=["TRIAGE", "TRANSFERRED"],
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
    Fetch patients whose visit's current_state is 'PHARMACY' or 'CONSULTATION' and next_state is 'BILLING'.
    """
    today = timezone.now().date()
    visits = Visit.objects.filter(
        next_state="BILLING",
        current_state__in=["PHARMACY", "CONSULTATION"],  # Include both states
        # visit_date=today  # Uncomment if you want to filter by today's date
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
    visits = Visit.objects.filter(
        patient=patientId,
        visit_date=today,
    ).order_by(
        "-visit_date"
    )  # Fetch all visits for the day, ordered by creation time
    print(visits)
    if not visits:
        return Response({"error": "No visits found for today"}, status=404)

    visit_data = []
    for visit in visits:
        triage = Triage.objects.filter(visit=visit).first()
        consultation = PhysicianNote.objects.filter(visit=visit).first()
        patient = Patient.objects.filter(id=patientId).first()
        lab = LabResult.objects.filter(visit=visit).first()
        medication = Medication.objects.filter(visit=visit).first()
        department = DepartmentSerializer(visit.department).data

        visit_data.append(
            {
                "visit_id": visit.visit_id,
                "department": department,
                "visit_type": visit.visit_type,
                "transfer_history": visit.transfer_history,
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
                        "total_cost": consultation.total_cost,
                        "prescription": consultation.prescription,
                        "lab_test_ordered": consultation.lab_tests_ordered,
                        "physician": (
                            consultation.physician.id
                            if consultation.physician
                            else None
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
                        "contact_number": patient.contact_number,
                    }
                    if patient
                    else None
                ),
                "lab_data": (
                    {"result": lab.result, "total_cost": lab.total_cost}
                    if lab
                    else None
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

    return Response(visit_data)


@api_view(["GET"])
def get_patient_history(request, patientId):
    # Fetch all visits for the patient and prefetch related objects
    visits = Visit.objects.filter(
        patient_id=patientId, current_state="BILLING", next_state="COMPLETED"
    ).prefetch_related(
        "triage",  # Prefetch related Triage objects
        "consultations",  # Correct related_name for Consultation
        "labs",  # Correct related_name for Lab
        "pharmacies",  # Correct related_name for Pharmacy
        "billings",  # Correct related_name for Billing
    )

    history = []

    for visit in visits:
        visit_data = {
            "visit_id": visit.visit_id,
            "visit_date": visit.visit_date,
            "current_state": visit.current_state,
            "transfer_history": visit.transfer_history,
            "next_state": visit.next_state,
            "total_cost": visit.total_cost,
            "visit_type": visit.visit_type,
            "department": visit.department.name if visit.department else None,
            "triage": None,  # Initialize triage as None
            "consultations": list(
                visit.consultations.all().values()
            ),  # Correct related_name
            "labs": list(visit.labs.all().values()),  # Correct related_name
            "pharmacies": list(visit.pharmacies.all().values()),  # Correct related_name
            "billings": list(visit.billings.all().values()),  # Correct related_name
        }

        # Access the related Triage object (if it exists)
        if hasattr(visit, "triage"):
            visit_data["triage"] = {
                "triage_id": visit.triage.triage_id,
                "vital_signs": visit.triage.vital_signs,
                "recorded_by": (
                    visit.triage.recorded_by.username
                    if visit.triage.recorded_by
                    else None
                ),
                "recorded_at": visit.triage.recorded_at,
            }

        history.append(visit_data)

    return Response(history)


from django.forms.models import model_to_dict


@api_view(["GET"])
def get_visit_details(request, visitId):
    visit = Visit.objects.prefetch_related(
        "triage",  # Prefetch related Triage objects
        "consultations",  # Ensure correct related_name for Consultation
        "labs",  # Ensure correct related_name for Lab
        "pharmacies",  # Ensure correct related_name for Pharmacy
        "billings",  # Ensure correct related_name for Billing
    ).get(visit_id=visitId)

    # Use model_to_dict to safely serialize the triage object
    triage_data = model_to_dict(visit.triage) if visit.triage else None

    visit_data = {
        "visit_id": visit.visit_id,
        "visit_date": visit.visit_date,
        "visit_type": visit.visit_type,
        "transfer_history": visit.transfer_history,
        "department": visit.department.name if visit.department else None,
        "triage": triage_data,
        "consultation": list(visit.consultations.all().values()),
        "lab": list(visit.labs.all().values()),
        "pharmacy": list(visit.pharmacies.all().values()),
        "billing": list(visit.billings.all().values()),
    }

    return Response(visit_data)


@api_view(["GET"])
def get_all_visits(request):
    """
    Fetch all visits.
    """
    visits = Visit.objects.prefetch_related(
        "triage", "consultations", "labs", "pharmacies", "billings"
    ).all()

    visit_data = []
    for visit in visits:
        visit_data.append(
            {
                "visit_id": visit.visit_id,
                "visit_date": visit.visit_date,
                "visit_type": visit.visit_type,
                "department": visit.department.name if visit.department else None,
                "transfer_history": visit.transfer_history,
                "visit_status": visit.visit_status,
                "patient_name": f"{visit.patient.first_name} {visit.patient.last_name}",
                "patient_id": visit.patient.id,
                "triage": None,
                "consultation": list(visit.consultations.all().values()),
                "lab": list(visit.labs.all().values()),
                "pharmacy": list(visit.pharmacies.all().values()),
                "billing": list(visit.billings.all().values()),
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
                "transfer_history": visit.transfer_history,
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


@api_view(["POST"])
def transfer_patient(request):
    """
    Transfer a patient from one department to another.
    """
    data = request.data
    visit_id = data.get("visit_id")
    new_department_id = data.get("new_department_id")
    referral_reason = data.get("referral_reason", "")
    transferred_by = data.get(
        "transferred_by"
    )  # ID of the doctor initiating the transfer

    try:
        visit = Visit.objects.get(visit_id=visit_id)
        new_department = Department.objects.get(id=new_department_id)
    except Visit.DoesNotExist:
        return Response({"error": "Visit not found"}, status=status.HTTP_404_NOT_FOUND)
    except Department.DoesNotExist:
        return Response(
            {"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND
        )

    # Create a new transfer entry with department names
    transfer_entry = {
        "from_department": visit.department.name if visit.department else "N/A",
        "to_department": new_department.name,
        "reason": referral_reason,
        "transferred_by": transferred_by,
        "transferred_at": timezone.now().isoformat(),
    }

    # Append the new transfer entry to the transfer_history
    if not visit.transfer_history:
        visit.transfer_history = []
    visit.transfer_history.append(transfer_entry)

    # Update the Visit model
    visit.department = new_department  # Set the new department
    visit.current_state = "TRANSFERRED"  # Update current state
    visit.next_state = (
        "CONSULTATION"  # Set next state to consultation in the new department
    )
    visit.save()

    return Response(
        {
            "message": "Patient transferred successfully",
            "transfer_history": visit.transfer_history,  # Return the updated transfer history
        },
        status=status.HTTP_200_OK,
    )
