from django.db import models

# Create your models here.

class Billing(models.Model):
    bill_id = models.AutoField(primary_key=True)
    visit = models.ForeignKey("visits.Visit", on_delete=models.CASCADE)
    consultation_cost = models.DecimalField(max_digits=10, decimal_places=2)
    laboratory_cost = models.DecimalField(max_digits=10, decimal_places=2)
    pharmacy_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    recorded_at = models.DateTimeField(auto_now_add=True)
    billed_by = models.ForeignKey(
        "accounts.Staff", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return f"Billing for Visit ID: {self.visit.visit_id} - Service: {self.service_name}"
