from rest_framework import serializers
from .models import StaffUser
from django.contrib.auth.hashers import make_password


class StaffUserSerializer(serializers.ModelSerializer):
    roles = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
    )
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = StaffUser
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "roles",
            "phone_number",
            "password",
            "is_staff",
            "is_active",
            "date_joined",
        ]
        extra_kwargs = {
            "username": {"required": False},  # Make username optional
        }

    def create(self, validated_data):
        roles = validated_data.pop("roles", [])
        # Generate username from first_name and last_name
        first_name = validated_data.get("first_name", "").strip().replace(" ", "")
        last_name = validated_data.get("last_name", "").strip().replace(" ", "")
        username = f"{first_name}-{last_name}".lower()
        validated_data["username"] = username
        # Set default password to '00000000'
        validated_data["password"] = make_password("00000000")
        user = super().create(validated_data)
        user.set_roles_list(roles)
        user.save()
        return user

    def update(self, instance, validated_data):
        roles = validated_data.pop("roles", None)
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        user = super().update(instance, validated_data)
        if roles is not None:
            user.set_roles_list(roles)
            user.save()
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["roles"] = instance.get_roles_list()
        return representation
