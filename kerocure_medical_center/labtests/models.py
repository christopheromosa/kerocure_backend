from django.db import models


# Create your models here.
class LabTest(models.Model):
    service = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=11, decimal_places=2)
    duration = models.DurationField()

    def __str__(self):
        return self.service
