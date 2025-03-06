from django.urls import path
from .views import LabTestListCreateView, LabTestDetailView, UploadLabTestView

urlpatterns = [
    path("labtests/", LabTestListCreateView.as_view(), name="labtest-list"),
    path("labtests/<int:pk>/", LabTestDetailView.as_view(), name="labtest-detail"),
    path("upload-lab-tests/", UploadLabTestView.as_view(), name="upload-lab-tests"),
]
