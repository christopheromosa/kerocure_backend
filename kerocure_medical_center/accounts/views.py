from rest_framework import viewsets
from .models import Staff
from .serializers import AccountSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

class AccountsViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = AccountSerializer


class StaffLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        # Default values
        user_id = user.id  # Use Django user ID by default
        role = None
        
        try:
            staff = Staff.objects.get(user=user)
            role = staff.role
            user_id = staff.id  # Override with Staff ID if found
        except Staff.DoesNotExist:
            if user.is_superuser:
                role = "Administrator"
            else:
                return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
        
        return Response({
            "token": token.key,
            "user_id": user_id,
            "username": user.username,
            "role": role,
        })
