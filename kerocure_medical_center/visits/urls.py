from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VisitViewSet,
    triage_patients,
    consultation_patients,
    lab_patients,
    pharmacy_patients,
    billing_patients,
    get_today_visit,
)


router = DefaultRouter()
router.register(r"visits", VisitViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api/triage-patients/", triage_patients, name="triage-patients"),
    path(
        "api/consultation-patients/",
        consultation_patients,
        name="consultation-patients",
    ),
    path("api/lab-patients/", lab_patients, name="lab-patients"),
    path("api/pharmacy-patients/", pharmacy_patients, name="pharmacy-patients"),
    path("api/billing-patients/", billing_patients, name="billing-patients"),
    path(
        "api/visit/today/<int:patientId>/",
        get_today_visit,
        name="get_today_visit",
    ),
]
