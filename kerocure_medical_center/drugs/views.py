from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Drug
from .serializers import DrugSerializer
from rest_framework.viewsets import ModelViewSet


class DrugViewSet(ModelViewSet):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer

    def perform_create(self, serializer):
        serializer.save()
    def get_queryset(self):
        query = self.request.query_params.get("query", "")
        return Drug.objects.filter(drug_name__icontains=query)


class DrugListCreateView(generics.ListCreateAPIView):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer


class DrugDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
