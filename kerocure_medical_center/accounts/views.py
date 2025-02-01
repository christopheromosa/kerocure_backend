from rest_framework import viewsets
from .models import Staff
from .serializers import AccountSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status

class AccountsViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = AccountSerializer

    def perform_create(self, serializer):
        """
        This method is overridden to call `create` method of the serializer
        which handles generating username and password.
        """
        if User.objects.filter(username=serializer.validated_data["username"]).exists():
            return Response({"error","Username already exists"},status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=serializer.validated_data["username"], password=serializer.validated_data["password"])
        staff.user = user
        staff = serializer.save()
        return staff



