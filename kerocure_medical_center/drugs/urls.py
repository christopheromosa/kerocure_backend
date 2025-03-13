from django.urls import path
from .views import DrugListCreateView, DrugDetailView,DrugViewSet,UploadDrugStockView,DispenseDrugView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r"drugs", DrugViewSet)
urlpatterns = [
    path("drugs/", DrugListCreateView.as_view(), name="drug-list"),
    path("drugs/<int:pk>/", DrugDetailView.as_view(), name="drug-detail"),
     path("upload-drug-stock/", UploadDrugStockView.as_view(), name="upload-drug-stock"),
     path("dispense-drug/", DispenseDrugView.as_view(), name="dispense-drug"),
    
]
