from rest_framework.viewsets import ModelViewSet
from .models import Medication
from .serializers import PharmacySerializer
from rest_framework.decorators import api_view
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import generics, status
from drugs.models import Drug


class PharmacyViewSet(ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = PharmacySerializer

    


@api_view(["GET"])
def medication_fee(request, visitId):
    medication = Medication.objects.filter(visit=visitId).first()

    if not medication:
        return Response({"error": "No consultation cost found for today"}, status=404)
    return Response({"cost": medication.cost})
