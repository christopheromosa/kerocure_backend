from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Staff(models.Model):
    ROLE_CHOICES = [
        ("Triage", "Triage"),
        ("Doctor", "Doctor"),
        ("Nurse", "Nurse"),
        ("Lab Technician", "Lab Technician"),
        ("Pharmacist", "Pharmacist"),
        ("Administrator", "Administrator"),
        ("Billing", "Billing"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default="Other",
    )
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # Store password hash (not plain text)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True, related_name="staff")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

    class Meta:
        ordering = ["last_name", "first_name"]
