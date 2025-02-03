from rest_framework import serializers
from .models import Visit

class VisitSerializer(serializers.ModelSerializer):
    visit_date = serializers.DateField(format="%Y-%m-%d",read_only=True)

    class Meta:
        model = Visit
        fields = "__all__"
