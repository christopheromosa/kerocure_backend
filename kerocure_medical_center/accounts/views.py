from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Staff
from .serializers import AccountSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password

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
class StaffPasswordResetView(APIView):
    """
    Allows a staff member to reset their password.
    """
    permission_classes = [IsAuthenticated]  # Require authentication

    def post(self, request):
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not new_password or not confirm_password:
            return Response({"error": "Both password fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the logged-in user
        user = request.user

        try:
            staff = Staff.objects.get(user=user)
        except Staff.DoesNotExist:
            return Response({"error": "Staff account not found"}, status=status.HTTP_404_NOT_FOUND)

        # Reset password for both User and Staff models
        hashed_password = make_password(new_password)
        user.set_password(new_password)  # Securely hash password
        user.save()

        staff.password = hashed_password  # Sync staff password (optional)
        staff.save()

        # Invalidate old authentication tokens
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)

        return Response({"message": "Password reset successful", "new_token": token.key}, status=status.HTTP_200_OK)
