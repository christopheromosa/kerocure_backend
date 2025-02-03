from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PharmacyViewSet,medication_fee

router = DefaultRouter()
router.register(r"pharmacy", PharmacyViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("medication-fee/<int:visitId>", medication_fee, name="medication-fee"),
]
