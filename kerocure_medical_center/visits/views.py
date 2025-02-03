from django.shortcuts import render
from .models import Visit
from rest_framework.viewsets import ModelViewSet
from .serializers import VisitSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from patients.serializers import PatientSerializer
from rest_framework import status
from django.utils import timezone


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
            patient_id=patient_id, visit_date__date=today
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
        current_state="triage", next_state="consultation"
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
        current_state="consultation", next_state="lab"
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
        current_state="lab", next_state="consultation"
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
        current_state="consultation", next_state="pharmacy"
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
        current_state="pharmacy", next_state="billing"
    ).select_related("patient")
    patients = [visit.patient for visit in visits]
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_visit_id_by_patient_id_date(request):
    patient_id = request.data.get("patient")
    today = timezone.now().date()
    visit = Visit.objects.filter(patient_id=3, visit_date__date=today)
    print(visit)
    return Response(visit)
