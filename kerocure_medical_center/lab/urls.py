from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LabViewSet, laboratory_fee

router = DefaultRouter()
router.register(r"lab", LabViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("laboratory-fee/<int:visitId>", laboratory_fee, name="laboratory-fee"),
]
