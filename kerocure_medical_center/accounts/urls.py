from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountsViewSet, StaffLoginView,StaffPasswordResetView


router = DefaultRouter()
router.register(r"accounts", AccountsViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "api/login/", StaffLoginView.as_view(), name="staff-login"
    ),  # Include this line to enable token-based authentication
    path("staff/reset-password/", StaffPasswordResetView.as_view(), name="staff-reset-password"),
]
