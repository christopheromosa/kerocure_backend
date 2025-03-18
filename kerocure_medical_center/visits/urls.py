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
    admin_patients,
    get_patient_history,
    get_visit_details,
    triage_patients_department,
    get_all_visits,
    transfer_patient
)


router = DefaultRouter()
router.register(r"visits", VisitViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api/triage-patients/", triage_patients, name="triage-patients"),
    path(
        "api/triage-department-patients/<int:department_id>",
        triage_patients_department,
        name="triage-department_patients",
    ),
    path(
        "api/consultation-patients/",
        consultation_patients,
        name="consultation-patients",
    ),
    path("api/lab-patients/", lab_patients, name="lab-patients"),
    path("api/pharmacy-patients/", pharmacy_patients, name="pharmacy-patients"),
    path("api/billing-patients/", billing_patients, name="billing-patients"),
    path("api/admin-patients/", admin_patients, name="admin-patients"),
    path(
        "api/visit/today/<int:patientId>/",
        get_today_visit,
        name="get_today_visit",
    ),
    path(
        "api/patient_visits/<int:patientId>/",
        get_patient_history,
        name="patient-visits",
    ),
    path(
        "api/patient_visits_details/<int:visitId>/",
        get_visit_details,
        name="patient-visit-details",
    ),
    path("api/all-visits/", get_all_visits, name="get-all-visits"),
    path("api/transfer-patient/", transfer_patient, name="transfer-patient"),
]
