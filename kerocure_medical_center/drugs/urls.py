from django.urls import path
from .views import DrugListCreateView, DrugDetailView,DrugViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r"drugs", DrugViewSet)
urlpatterns = [
    path("drugs/", DrugListCreateView.as_view(), name="drug-list"),
    path("drugs/<int:pk>/", DrugDetailView.as_view(), name="drug-detail"),
]
