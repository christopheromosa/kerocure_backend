from django.urls import path
from .views import DiseaseListCreateView, DiseaseSearchView,DiseaseRetrieveUpdateDestroyView

urlpatterns = [
    path("diseases/", DiseaseListCreateView.as_view(), name="disease-list-create"),
    path("diseases/search/", DiseaseSearchView.as_view(), name="disease-search"),
    path("diseases/<int:pk>/", DiseaseRetrieveUpdateDestroyView.as_view(), name="disease-retrieve-update-destroy"),
]
