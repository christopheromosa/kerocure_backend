from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConsultationViewSet

router = DefaultRouter()
router.register(r"consultation", ConsultationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
