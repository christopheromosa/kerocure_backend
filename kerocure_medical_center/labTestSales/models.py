from django.db import models
from django.utils import timezone
from labtests.models import LabTest


# Create your models here.
class LabTestSale(models.Model):
    service = models.CharField(default="",null=True,max_length=255)
    operation_count = models.PositiveIntegerField(default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.service} - {self.operation_count} operations - {self.total_amount} on {self.date}"
