from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission


class StaffUser(AbstractUser):
    ROLE_CHOICES = [
        ("Triage", "Triage"),
        ("Doctor", "Doctor"),
        ("Nurse", "Nurse"),
        ("Lab Technician", "Lab Technician"),
        ("Pharmacist", "Pharmacist"),
        ("Administrator", "Administrator"),
        ("Billing", "Billing"),
    ]

    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="Triage")
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    # Add unique related_name to avoid clashes
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="staffuser_groups",  # Unique related_name
        related_query_name="staffuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="staffuser_permissions",  # Unique related_name
        related_query_name="staffuser",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"
