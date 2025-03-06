from django.db import models


# Create your models here.
class Patient(models.Model):
    SEX_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=6, choices=SEX_CHOICES, default="")
    dob = models.DateField()
    residence = models.CharField(max_length=255, default="")
    contact_number = models.CharField(max_length=15)
    next_of_kin_name = models.CharField(max_length=255, default="")
    next_of_kin_contact_number = models.CharField(max_length=15, default="")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
