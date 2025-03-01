from rest_framework.viewsets import ModelViewSet
from .models import Medication
from .serializers import PharmacySerializer
from rest_framework.decorators import api_view
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import generics, status

class PharmacyViewSet(ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = PharmacySerializer

    def perform_create(self, serializer):
        drug_id = self.request.data.get("drug")
        quantity_dispensed = self.request.data.get("quantity_dispensed")
        drug = Drug.objects.get(id=drug_id)

        if quantity_dispensed > drug.quantity:
            return Response(
                {"error": "Not enough stock to dispense."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(drug=drug)


@api_view(["GET"])
def medication_fee(request, visitId):
    medication = Medication.objects.filter(visit=visitId).first()

    if not medication:
        return Response({"error": "No consultation cost found for today"}, status=404)
    return Response({"cost": medication.cost})
