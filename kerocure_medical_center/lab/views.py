from rest_framework.viewsets import ModelViewSet
from .models import LabResult
from .serializers import LabSerializer
from rest_framework.decorators import api_view
from django.utils import timezone
from rest_framework.response import Response

class LabViewSet(ModelViewSet):
    queryset = LabResult.objects.all()
    serializer_class = LabSerializer

    def perform_create(self, serializer):
        serializer.save()


@api_view(["GET"])
def laboratory_fee(request, visitId):
    laboratory = LabResult.objects.filter(visit=visitId).first()

    if not laboratory:
        return Response({"error": "No consultation cost found for today"}, status=404)
    return Response({"cost": laboratory.total_cost})
