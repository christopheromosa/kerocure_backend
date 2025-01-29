from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .models import Patient
from .serializers import PatientSerializer
from visits.models import Visit


class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def perform_create(self, serializer):
        patient = serializer.save()
        if not Visit.objects.filter(patient=patient):
         Visit.objects.create(patient=patient,current_state="TRIAGE",next_state="CONSULTATION",total_cost=0)



