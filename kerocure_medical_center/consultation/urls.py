from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConsultationViewSet,consultation_fee

router = DefaultRouter()
router.register(r"consultation", ConsultationViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("consultation-fee/<int:visitId>",consultation_fee,name="consultation-fee")
]
