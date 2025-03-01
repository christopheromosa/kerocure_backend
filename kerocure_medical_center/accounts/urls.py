from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StaffUserViewSet, StaffLoginView, StaffPasswordResetView

router = DefaultRouter()
router.register(r"accounts", StaffUserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api/login/", StaffLoginView.as_view(), name="staff-login"),
    path(
        "staff/reset-password/",
        StaffPasswordResetView.as_view(),
        name="staff-reset-password",
    ),
]
