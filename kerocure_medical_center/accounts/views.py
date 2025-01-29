from rest_framework import viewsets
from .models import Staff
from .serializers import AccountSerializer


class AccountsViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = AccountSerializer

    def perform_create(self, serializer):
        """
        This method is overridden to call `create` method of the serializer
        which handles generating username and password.
        """
        staff = serializer.save()
        return staff
