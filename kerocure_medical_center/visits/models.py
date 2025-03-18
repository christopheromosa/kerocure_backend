from django.db import models


# Create your models here.
class Visit(models.Model):
    VISIT_CHOICES = [("Outpatient", "Outpatient"), ("Inpatient", "Inpatient")]
    visit_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        "patients.Patient", on_delete=models.CASCADE, related_name="visits"
    )
    visit_date = models.DateField(auto_now_add=True)
    current_state = models.CharField(max_length=50)
    next_state = models.CharField(max_length=50)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    visit_type = models.CharField(max_length=50, choices=VISIT_CHOICES, default="Outpatient")
    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.SET_NULL,
        default=2,
        blank=True,
        null=True,
        related_name="visits",  # To fetch all visits related to a patient in a single query
    )
    transfer_history = models.JSONField(  # JSON field to store transfer history
            default=list,
            blank=True,
            null=True,
            help_text="Stores transfer history as a list of objects with keys: from_department, to_department, reason, transferred_by, transferred_at",
        ) 
    visit_status = models.CharField(
            max_length=20, blank=True, default="pending"
        )

    def __str__(self):
        return f"Visit ID: {self.visit_id} for {self.patient}"
