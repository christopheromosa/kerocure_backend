from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

StaffUser = get_user_model()


class StaffUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    is_staff = serializers.BooleanField(default=False)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = StaffUser
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "role",
            "phone_number",
            "password",
            "is_staff",
            "is_active",
            "date_joined",
        ]

    def create(self, validated_data):
        validated_data["password"] = make_password(
            validated_data.get("password", "000000")
        )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)
