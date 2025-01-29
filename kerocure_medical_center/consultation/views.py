# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .models import PhysicianNote
from .serializers import ConsultationSerializer
from visits.models import Visit


class ConsultationViewSet(ModelViewSet):
    queryset = PhysicianNote.objects.all()
    serializer_class = ConsultationSerializer
    
    def perform_create(self, serializer):
        serializer.save()
   
        