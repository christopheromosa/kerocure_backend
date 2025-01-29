from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TriageViewSet

router = DefaultRouter()
router.register(r"triage", TriageViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
