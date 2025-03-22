from django.db import models
from django.utils import timezone
from drugs.models import Drug


class DrugSale(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='sales')
    quantity_sold = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.drug.drug_name} - {self.quantity_sold} units - {self.total_amount} on {self.date}"

