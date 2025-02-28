from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet

router = DefaultRouter()
router.register(r"departments", DepartmentViewSet)  # API endpoint

urlpatterns = [
    path("", include(router.urls)),  # This includes all CRUD URLs
]
