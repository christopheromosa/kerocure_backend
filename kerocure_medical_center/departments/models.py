from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=True, default=1,null=True)

    def __str__(self):
        return self.name
