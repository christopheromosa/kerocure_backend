from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import validate_comma_separated_integer_list


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
    roles = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Comma-separated list of roles",
    )
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="staffuser_groups",
        related_query_name="staffuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="staffuser_permissions",
        related_query_name="staffuser",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.roles})"

    def get_roles_list(self):
        """Helper method to return roles as a list."""
        return self.roles.split(",") if self.roles else []

    def set_roles_list(self, roles):
        """Helper method to set roles from a list."""
        self.roles = ",".join(roles) if roles else None
