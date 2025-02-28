from django.db import models


# Create your models here.
class Drug(models.Model):
    drug_name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.drug_name
