from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Billing
from .serializers import BillingSerializer
from django.db.models import Sum, DateField
from django.db.models.functions import TruncDate

class BillingViewSet(ModelViewSet):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer

    def perform_create(self, serializer):
        serializer.save()
        
@api_view(["GET"])
def total_revenue_per_day(request):
    revenue_per_day = (
        Billing.objects.annotate(date=TruncDate('recorded_at')).values("date").annotate(total_cost=Sum("total_cost")).order_by("date")
    )
   
    return Response(revenue_per_day)
