from django.db import models

# Create your models here.
class Visit(models.Model):
    visit_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey("patients.Patient", on_delete=models.CASCADE)
    visit_date = models.DateTimeField(auto_now_add=True)
    current_state = models.CharField(max_length=50)
    next_state = models.CharField(max_length=50)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Visit ID: {self.visit_id} for {self.patient}"
