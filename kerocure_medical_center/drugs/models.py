from django.db import models


# Create your models here.
class Drug(models.Model):
    drug_name = models.CharField(max_length=255)
    cost = models.IntegerField(null=True)
    quantity = models.PositiveIntegerField(default=0)  # Track the quantity of the drug
    status = models.CharField(max_length=20, default="Available")

    def __str__(self):
        return self.drug_name

    def update_status(self):
        """Update the status based on the quantity."""
        if self.quantity <= 0:
            self.status = "Out of Stock"
        else:
            self.status = "Available"
        self.save()

    def dispense_drug(self, quantity_dispensed):
        """Deduct the quantity dispensed and update the status."""
        if quantity_dispensed > self.quantity:
            raise ValueError("Not enough stock to dispense.")
        self.quantity -= quantity_dispensed
        self.update_status()

    def calculate_cost(self, quantity):
        """Calculate the total cost for the given quantity."""
        return self.cost * quantity
