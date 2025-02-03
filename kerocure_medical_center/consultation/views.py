# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .models import PhysicianNote
from .serializers import ConsultationSerializer
from visits.models import Visit
from rest_framework.decorators import api_view
from django.utils import timezone
from rest_framework.response import Response


class ConsultationViewSet(ModelViewSet):
    queryset = PhysicianNote.objects.all()
    serializer_class = ConsultationSerializer

    def perform_create(self, serializer):
        serializer.save()


@api_view(["GET"])
def consultation_fee(request, visitId):
    consultation = PhysicianNote.objects.filter(visit=visitId).first()

    if not consultation:
        return Response({"error": "No consultation cost found for today"}, status=404)
    return Response({"cost":consultation.total_cost})
