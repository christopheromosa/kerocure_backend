from django.urls import path
from .views import DiseaseListCreateView, DiseaseSearchView

urlpatterns = [
    path("diseases/", DiseaseListCreateView.as_view(), name="disease-list-create"),
    path("diseases/search/", DiseaseSearchView.as_view(), name="disease-search"),
]
