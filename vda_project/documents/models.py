from django.db import models
from vehicles.models import Vehicle

class Document(models.Model):
    DOC_TYPES = [
        ("RCA", "RCA"),
        ("ITP", "ITP"),
        ("ROV", "Rovinieta"),
    ]
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="documents")
    doc_type = models.CharField(max_length=3, choices=DOC_TYPES)
    expires_on = models.DateField()
    file = models.FileField(upload_to="docs/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["expires_on"]

    def __str__(self):
        return f"{self.vehicle} - {self.doc_type} - {self.expires_on}"

