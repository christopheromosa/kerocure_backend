from rest_framework import serializers
from .models import Visit

class VisitSerializer(serializers.ModelSerializer):
    visit_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Visit
        fields = "__all__"
