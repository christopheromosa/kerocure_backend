from django.db import models
from accounts.models import StaffUser


# Create your models here.
class Triage(models.Model):
    triage_id = models.AutoField(primary_key=True)
    visit = models.OneToOneField("visits.Visit", on_delete=models.CASCADE)
    vital_signs = models.JSONField()  # Using JSONField for storing vital signs
    recorded_by = models.ForeignKey(
        StaffUser, on_delete=models.SET_NULL, null=True, blank=True
    )
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Triage for Visit ID: {self.visit.visit_id}"
