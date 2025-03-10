from rest_framework import generics
from .models import Disease
from .serializers import DiseaseSerializer
from rest_framework.response import Response
from rest_framework import status


class DiseaseListCreateView(generics.ListCreateAPIView):
    queryset = Disease.objects.all().order_by("-id")
    serializer_class = DiseaseSerializer


class DiseaseSearchView(generics.ListAPIView):
    serializer_class = DiseaseSerializer

    def get_queryset(self):
        query = self.request.query_params.get("search", "")
        return Disease.objects.filter(name__icontains=query)
