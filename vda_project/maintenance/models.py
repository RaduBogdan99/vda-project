from django.db import models
from vehicles.models import Vehicle # Importăm modelul Vehicul

class Maintenance(models.Model):
    # --- Legătura cu Vehiculul ---
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='maintenance_records', # Numele relației
        verbose_name="Vehicul"
    )

    # --- Detalii Operațiune ---
    date = models.DateField(verbose_name="Data operațiunii")

    odometer = models.PositiveIntegerField(
        verbose_name="Kilometraj (km)",
        help_text="Kilometrajul la momentul operațiunii"
    )

    cost = models.DecimalField(
        max_digits=8, # Permite un cost de până la 999,999.99
        decimal_places=2, # Cu 2 zecimale
        verbose_name="Cost (RON)",
        null=True,
        blank=True # Costul este opțional
    )

    notes = models.TextField(
        verbose_name="Descriere / Notițe",
        help_text="Ex: Schimb ulei și filtru aer, Plăcuțe frână față"
    )

    # Opțional: atașament (conform planului tău)
    attachment = models.FileField(
        upload_to='maintenance_attachments/',
        verbose_name="Atașament (Factură)",
        blank=True,
        null=True
    )

    # Date de trasabilitate
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # ex: "Schimb ulei - 150000 km"
        return f"{self.notes[:50]}... ({self.odometer} km)"

    class Meta:
        # Ordonăm de la cea mai recentă operațiune
        ordering = ['-date', '-odometer']


class MaintenanceAlert(models.Model):
    """
    Stochează o regulă de mentenanță recurentă (ex: Schimb ulei la 10k km / 12 luni)
    și când a fost efectuată ultima dată.
    """
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='maintenance_alerts',
        verbose_name="Vehicul"
    )

    description = models.CharField(
        max_length=200, 
        verbose_name="Descriere Operațiune",
        help_text="Ex: Schimb ulei și filtru, Schimb distribuție"
    )

    # --- Intervale (oricare se atinge primul) ---
    km_interval = models.PositiveIntegerField(
        verbose_name="Interval Kilometri (km)",
        null=True, blank=True, # Poate fi o alertă bazată doar pe timp
        help_text="Ex: 10000"
    )
    months_interval = models.PositiveIntegerField(
        verbose_name="Interval Timp (luni)",
        null=True, blank=True, # Poate fi o alertă bazată doar pe km
        help_text="Ex: 12"
    )

    # --- Când a fost efectuată ULTIMA DATĂ ---
    last_performed_date = models.DateField(verbose_name="Data ultimei operațiuni")
    last_performed_odometer = models.PositiveIntegerField(
        verbose_name="Kilometrajul la ultima operațiune"
    )

    def __str__(self):
        return f"Alertă: {self.description} pentru {self.vehicle.license_plate}"

    # ACESTA ESTE BLOCUL CORECTAT
    class Meta:
        # Ordonăm după data ultimei operațiuni
        ordering = ['-last_performed_date']