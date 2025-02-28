from django.db import models


# Create your models here.
class Visit(models.Model):
    VISIT_CHOICES = [("Visit", "Visit"), ("Revisit", "Revisit")]
    visit_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey("patients.Patient", on_delete=models.CASCADE)
    visit_date = models.DateField(auto_now_add=True)
    current_state = models.CharField(max_length=50)
    next_state = models.CharField(max_length=50)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    visit_type = models.CharField(max_length=50, choices=VISIT_CHOICES, default="")
    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.SET_NULL,
        default=2,
        blank=True,
        null=True,
        related_name="visits",  # To fetch all visits related to a patient in a single query
    )

    def __str__(self):
        return f"Visit ID: {self.visit_id} for {self.patient}"
