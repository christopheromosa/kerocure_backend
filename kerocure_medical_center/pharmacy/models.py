from django.db import models
from accounts.models import StaffUser


# Create your models here.
class Medication(models.Model):
    medication_id = models.AutoField(primary_key=True)
    visit = models.ForeignKey("visits.Visit", on_delete=models.CASCADE)
    note = models.ForeignKey("consultation.PhysicianNote", on_delete=models.CASCADE)
    prescriptions = models.JSONField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    dispensed_by = models.ForeignKey(
        StaffUser, on_delete=models.SET_NULL, null=True, blank=True
    )
    dispensed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Medication: {self.medication_id} for Visit ID: {self.visit.visit_id}"

    def save(self, *args, **kwargs):
        """Calculate the total cost and update the drug quantity."""
        self.total_cost = self.drug.calculate_cost(self.quantity_dispensed)
        super().save(*args, **kwargs)
        self.drug.dispense_drug(self.quantity_dispensed)
