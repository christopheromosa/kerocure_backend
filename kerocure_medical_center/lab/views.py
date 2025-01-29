from rest_framework.viewsets import ModelViewSet
from .models import LabResult
from .serializers import LabSerializer


class LabViewSet(ModelViewSet):
    queryset = LabResult.objects.all()
    serializer_class = LabSerializer

    def perform_create(self, serializer):
        serializer.save()
