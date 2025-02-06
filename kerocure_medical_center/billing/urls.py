from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BillingViewSet,total_revenue_per_day

router = DefaultRouter()
router.register(r"billing", BillingViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api/total-revenue-per-day/", total_revenue_per_day, name="total-revenue-per-day")
]
