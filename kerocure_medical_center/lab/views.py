from rest_framework.viewsets import ModelViewSet
from .models import LabResult
from .serializers import LabSerializer
from rest_framework.decorators import api_view
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status  

class LabViewSet(ModelViewSet):
    queryset = LabResult.objects.all().order_by("-result_id") 
    serializer_class = LabSerializer

    def perform_create(self, serializer):
        serializer.save()


@api_view(["GET"])
def laboratory_fee(request, visitId):
    laboratory = LabResult.objects.filter(visit=visitId).first()

    if not laboratory:
        return Response({"error": "No consultation cost found for today"}, status=404)
    return Response({"cost": laboratory.total_cost})
    
# New view to check for existing lab records by visit_id
@api_view(["GET"])
def check_lab_record(request, visit_id):
    try:
        lab_record = LabResult.objects.filter(visit=visit_id).first()
        if lab_record:
            # Return the existing lab record
            serializer = LabSerializer(lab_record)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # No lab record found for the given visit_id
            return Response(
                {"message": "No lab record found for this visit."},
                status=status.HTTP_404_NOT_FOUND,
            )
    except Exception as e:
        return Response(
            {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
