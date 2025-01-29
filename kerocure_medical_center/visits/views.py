from django.shortcuts import render
from .models import Visit
from rest_framework.viewsets import ModelViewSet
from .serializers import VisitSerializer

# Create your views here.
class VisitViewSet(ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
