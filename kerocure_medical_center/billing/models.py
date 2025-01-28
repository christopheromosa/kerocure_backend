from django.db import models

# Create your models here.

class Billing(models.Model):
    bill_id = models.AutoField(primary_key=True)
    visit = models.ForeignKey("patients.Visit", on_delete=models.CASCADE)
    service_name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Billing for Visit ID: {self.visit.visit_id} - Service: {self.service_name}"
