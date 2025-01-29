from rest_framework import serializers
from .models import Staff
from django.contrib.auth.hashers import make_password
from .utils import generate_username, generate_password


class AccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(read_only=True)

    # Only allow writing to the password field

    class Meta:
        model = Staff
        fields = [
            "first_name",
            "last_name",
            "role",
            "phone_number",
            "username",
            "password",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        """
        Override the create method to generate the username and password
        and hash the password before saving the staff object.
        """
        # Generate and assign the username automatically
        username = generate_username(validated_data)

        # Generate the password automatically
        password = generate_password(validated_data)

        # Hash the password before saving to the database
        validated_data["password"] = make_password(password)

        # Create the staff object
        staff = Staff.objects.create(username=username, **validated_data)

        # Store the plain password temporarily for the response
        self._plain_password = password  # Temporarily store the plain password

        return staff

    def to_representation(self, instance):
        """
        Customize the response to include the plain password.
        """
        # Get the default representation
        representation = super().to_representation(instance)

        # Add the plain password to the response data
        representation["password"] = getattr(self, "_plain_password", None)

        return representation
