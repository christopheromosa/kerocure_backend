from django.db import models


# Create your models here.
class LabResult(models.Model):
    result_id = models.AutoField(primary_key=True)
    visit = models.ForeignKey("patients.Visit", on_delete=models.CASCADE)
    note = models.ForeignKey("consultation.PhysicianNote", on_delete=models.CASCADE)
    test_name = models.CharField(max_length=255)
    result = models.TextField()
    recorded_by = models.ForeignKey("accounts.Staff", on_delete=models.SET_NULL, null=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Lab Result for Visit ID: {self.visit.visit_id} - Test: {self.test_name}"
        )
