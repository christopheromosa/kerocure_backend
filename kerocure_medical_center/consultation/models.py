from django.db import models
from accounts.models import StaffUser


# Create your models here.
class PhysicianNote(models.Model):
    note_id = models.AutoField(primary_key=True)
    visit = models.ForeignKey(
        "visits.Visit", on_delete=models.CASCADE, related_name="consultations"
    )

    triage = models.ForeignKey("triage.Triage", on_delete=models.SET_NULL, null=True)
    medical_history = models.JSONField(default=list, blank=True, null=True)
    diagnosis = models.TextField(default=list,blank=True, null=True)
    disease = models.CharField(default="", blank=True)
    prescription = models.JSONField(
        blank=True, null=True
    )  # Storing prescriptions as JSON
    lab_tests_ordered = models.JSONField(
        default=list, blank=True, null=True
    )  # Storing lab tests ordered as JSON
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=200.00)
    physician = models.ForeignKey( # Current physician handling the note
        StaffUser, on_delete=models.SET_NULL, null=True, blank=True,related_name="authored_notes"
    )
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Physician Note for Visit ID: {self.visit.visit_id}"
