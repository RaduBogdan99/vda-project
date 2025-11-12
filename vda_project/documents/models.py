from django.db import models
from vehicles.models import Vehicle  # Importăm modelul Vehicul


class Document(models.Model):
    # Definim opțiunile pentru tipul de document
    # Acesta este un mod curat de a crea un meniu dropdown
    class DocumentType(models.TextChoices):
        RCA = "RCA", "Asigurare RCA"
        ITP = "ITP", "Inspecție Tehnică Periodică"
        ROVINIETA = "ROVINIETA", "Rovinietă"
        CASCO = "CASCO", "Asigurare CASCO"
        OTHER = "OTHER", "Alt Document"

    # --- Legătura cu Vehiculul ---
    # Fiecare document aparține unui singur vehicul
    # Dacă ștergem vehiculul, se șterg și documentele asociate
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="documents", verbose_name="Vehicul"
    )

    # --- Detalii Document ---
    document_type = models.CharField(
        max_length=20,
        choices=DocumentType.choices,
        default=DocumentType.OTHER,
        verbose_name="Tip Document",
    )

    issue_date = models.DateField(
        verbose_name="Data emiterii", null=True, blank=True  # Permitem să fie gol
    )

    expiry_date = models.DateField(
        verbose_name="Data expirării",
        null=True,  # Important pentru documente care nu expiră (ex: factură)
        blank=True,
    )

    notes = models.TextField(verbose_name="Notițe", blank=True)  # Câmp opțional

    # Opțional: atașament (conform planului tău)
    # Vom seta un folder unde se încarcă fișierele
    attachment = models.FileField(
        upload_to="document_attachments/",
        verbose_name="Atașament (PDF/Poză)",
        blank=True,
        null=True,
    )

    # Date de trasabilitate
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # ex: "RCA (DJ 01 ABC) - Expiră la..."
        return f"{self.get_document_type_display()} ({self.vehicle.license_plate})"

    class Meta:
        # Ordonăm documentele după data expirării, cele mai apropiate prima dată
        ordering = ["expiry_date"]
