from django.db import models

# Create your models here.
class Medication(models.Model):
    medication_id = models.AutoField(primary_key=True)
    visit = models.ForeignKey("visits.Visit", on_delete=models.CASCADE)
    note = models.ForeignKey("consultation.PhysicianNote", on_delete=models.CASCADE)
    prescriptions =  models.JSONField(blank=True , null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    dispensed_by = models.ForeignKey(
        "accounts.Staff", on_delete=models.SET_NULL, null=True
    )
    dispensed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Medication: {self.medication_id} for Visit ID: {self.visit.visit_id}"

