from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, VisitViewSet

router = DefaultRouter()
router.register('patients', PatientViewSet)
router.register('visits', VisitViewSet)

urlpatterns = [
    path('', include(router.urls)),
]