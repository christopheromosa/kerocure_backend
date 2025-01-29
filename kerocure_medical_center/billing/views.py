from rest_framework.viewsets import ModelViewSet
from .models import Billing
from .serializers import BillingSerializer
class BillingViewSet(ModelViewSet):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer

    def perform_create(self, serializer):
        serializer.save()
