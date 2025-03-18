from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PharmacyViewSet,medication_fee,check_existing_medication

router = DefaultRouter()
router.register(r"pharmacy", PharmacyViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("medication-fee/<int:visitId>", medication_fee, name="medication-fee"),
    path(
            "check-existing-medication/<int:visit_id>/",
            check_existing_medication,
            name="check-existing-medication",
        ),
]
