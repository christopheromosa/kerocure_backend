from rest_framework.viewsets import ModelViewSet
from .models import Medication
from .serializers import PharmacySerializer
class PharmacyViewSet(ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = PharmacySerializer

    def perform_create(self, serializer):
        serializer.save()
