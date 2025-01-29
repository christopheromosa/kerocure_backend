from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LabViewSet

router = DefaultRouter()
router.register(r"lab", LabViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
