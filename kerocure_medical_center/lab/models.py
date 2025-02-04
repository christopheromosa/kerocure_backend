from django.db import models

# Create your models here.
class LabResult(models.Model):
    result_id = models.AutoField(primary_key=True)
    visit = models.ForeignKey("visits.Visit", on_delete=models.CASCADE)
    note = models.ForeignKey("consultation.PhysicianNote", on_delete=models.CASCADE)
    test_name = models.JSONField()
    result = models.JSONField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    recorded_by = models.ForeignKey("accounts.Staff", on_delete=models.SET_NULL, null=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return (
            f"Lab Result for Visit ID: {self.visit.visit_id} - Test: {self.test_name}"
        )
