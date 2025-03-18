from rest_framework.viewsets import ModelViewSet
from .models import Medication
from .serializers import PharmacySerializer
from rest_framework.decorators import api_view
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import generics, status
from drugs.models import Drug


class PharmacyViewSet(ModelViewSet):
    queryset = Medication.objects.all().order_by("-medication_id")
    serializer_class = PharmacySerializer 

@api_view(["GET"])
def medication_fee(request, visitId):
    medication = Medication.objects.filter(visit=visitId).first()

    if not medication:
        return Response({"error": "No consultation cost found for today"}, status=404)
    return Response({"cost": medication.cost})
@api_view(["GET"])
def check_existing_medication(request, visit_id):
    """
    Check if a medication record exists for the given visit_id.
    """
    try:
        # Query the Medication model for records with the given visit_id
        medication = Medication.objects.filter(visit=visit_id).first()

        if medication:
            # If a record exists, return it
            serializer = PharmacySerializer(medication)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # If no record exists, return a 404 response
            return Response(
                {"message": "No medication record found for this visit."},
                status=status.HTTP_404_NOT_FOUND,
            )
    except Exception as e:
        # Handle any unexpected errors
        return Response(
            {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
