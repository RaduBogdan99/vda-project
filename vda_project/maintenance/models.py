from django.db import models
from vehicles.models import Vehicle


class MaintenanceRecord(models.Model):
    TYPES = [
        ("OIL", "Oil change"),
        ("FLT", "Filters"),
        ("BRK", "Brakes"),
        ("GEN", "General"),
    ]
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="maintenance")
    date = models.DateField()
    odometer_km = models.PositiveIntegerField(null=True, blank=True)
    service_type = models.CharField(max_length=3, choices=TYPES)
    cost = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.vehicle} - {self.service_type} - {self.date}"
