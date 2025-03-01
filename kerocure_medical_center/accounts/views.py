from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import StaffUserSerializer
from rest_framework.decorators import action

StaffUser = get_user_model()


class StaffUserViewSet(viewsets.ModelViewSet):
    queryset = StaffUser.objects.all()
    serializer_class = StaffUserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def reset_password(self, request, pk=None):
        staff_user = self.get_object()
        new_password = request.data.get("new_password")
        if not new_password:
            return Response(
                {"error": "New password is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        staff_user.set_password(new_password)
        staff_user.save()
        return Response(
            {"message": "Password reset successful"}, status=status.HTTP_200_OK
        )


class StaffLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user_id": user.id,
                "username": user.username,
                "role": user.role,
            }
        )


class StaffPasswordResetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not new_password or not confirm_password:
            return Response(
                {"error": "Both password fields are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if new_password != confirm_password:
            return Response(
                {"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        user.set_password(new_password)
        user.save()

        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)

        return Response(
            {"message": "Password reset successful", "new_token": token.key},
            status=status.HTTP_200_OK,
        )
