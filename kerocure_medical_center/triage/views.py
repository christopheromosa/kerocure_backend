# Create your views here.
from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .models import Triage
from .serializers import TriageSerializer
from visits.models import Visit


class TriageViewSet(ModelViewSet):
    queryset = Triage.objects.all()
    serializer_class = TriageSerializer

    def perform_create(self, serializer):
        triage = serializer.save()
        # Extract the patient from the visit
        patient = triage.visit.patient
        # Ensure the patient has a visit; if not, create one
        if not Visit.objects.filter(patient=patient).exists():
            # Create a new visit for the patient
            Visit.objects.create(patient=patient, current_state="TRIAGE", next_state="CONSULTATION", total_cost=0)

        # update existing visit states
        visit = Visit.objects.filter(patient=patient).last()
        visit.current_state = "TRIAGE"
        visit.next_state = "CONSULTATION"
        visit.save()
