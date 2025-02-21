from rest_framework import serializers
from .models import Patient
from datetime import date


class PatientSerializer(serializers.ModelSerializer):

    age = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = "__all__"

    def get_age(self, obj):
        today = date.today()
        dob = obj.dob
        years = (
            today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        )
        # If the patient is less than 1 year old, return age in months and days
        if years == 0:
            months = today.month - dob.month
            days = today.day - dob.day

            # Adjust if the birth month is ahead in the year
            if months < 0:
                months += 12
                years -= 1
            # Adjust if birth day is ahead in the month
            if days < 0:
                from calendar import monthrange

                prev_month_days = monthrange(today.year, today.month - 1)[
                    1
                ]  # Days in previous month
                days += prev_month_days
                months -= 1
            return f"{months} months, {days} days" if months > 0 else f"{days} days old"
        # otherwise, return age in years and months
        return years
