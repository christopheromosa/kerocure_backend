from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .models import Patient
from .serializers import PatientSerializer
from visits.models import Visit
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all().order_by("-id")
    serializer_class = PatientSerializer

    def perform_create(self, serializer):
        patient = serializer.save()

    @action(detail=False, methods=["get"], url_path="check-duplicate")
    def check_duplicate(self, request):
        first_name = request.query_params.get("first_name", "").strip()
        last_name = request.query_params.get("last_name", "").strip()
        contact_number = request.query_params.get("contact_number", "").strip()

        if not (first_name and last_name and contact_number):
            return Response(
                {"error": "Missing required query parameters"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        exists = Patient.objects.filter(
            first_name__iexact=first_name,
            last_name__iexact=last_name,
            contact_number=contact_number,
        ).exists()

        return Response({"exists": exists})
