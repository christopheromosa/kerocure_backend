from django.db import models


# Create your models here.
class Patient(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob = models.DateField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Visit(models.Model):
    visit_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey("patients.Patient", on_delete=models.CASCADE)
    visit_date = models.DateTimeField(auto_now_add=True)
    current_state = models.CharField(max_length=50)
    next_state = models.CharField(max_length=50)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Visit ID: {self.visit_id} for {self.patient}"
