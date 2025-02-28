from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import LabTest
from .serializer import LabTestSerializer
from rest_framework.viewsets import ModelViewSet


class LabTestSet(ModelViewSet):
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer

    def perform_create(self, serializer):
        serializer.save()


class LabTestListCreateView(generics.ListCreateAPIView):
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer


class LabTestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer
