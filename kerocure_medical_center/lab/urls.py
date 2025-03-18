from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LabViewSet, laboratory_fee,check_lab_record

router = DefaultRouter()
router.register(r"lab", LabViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("laboratory-fee/<int:visitId>", laboratory_fee, name="laboratory-fee"),
    # New URL for checking existing lab records
    path("check-lab-record/<int:visit_id>/", check_lab_record, name="check-lab-record"),
    
]
