from rest_framework import viewsets
from .models import Staff
from .serializers import AccountSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class AccountsViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = AccountSerializer


class StaffLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        
        # Fetch the associated staff profile
        try:
            staff = Staff.objects.get(user=user)
            role = staff.role
        except Staff.DoesNotExist:
            role = None
            
        return Response({"token": token.key,'user_id':user.pk,"username": user.username, "role": role})
        
        
        
    



