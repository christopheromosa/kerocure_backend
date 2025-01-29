from django.db import models


# Create your models here.
class PhysicianNote(models.Model):
    note_id = models.AutoField(primary_key=True)
    visit = models.ForeignKey("visits.Visit", on_delete=models.CASCADE)
    triage = models.ForeignKey("triage.Triage", on_delete=models.SET_NULL, null=True)
    diagnosis = models.TextField()
    prescription = models.JSONField()  # Storing prescriptions as JSON
    lab_tests_ordered = models.JSONField()  # Storing lab tests ordered as JSON
    physician = models.ForeignKey("accounts.Staff", on_delete=models.SET_NULL, null=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Physician Note for Visit ID: {self.visit.visit_id}"
