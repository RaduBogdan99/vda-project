from django.db import models
from django.conf import settings # Ne trebuie pentru a ne lega de User

class Vehicle(models.Model):
    # --- Legătura cu Utilizatorul ---
    # Aceasta este linia cheie.
    # Conectează fiecare vehicul de un utilizator specific.
    # related_name='vehicles' ne va lăsa să găsim ușor toate vehiculele unui user.
    # on_delete=models.CASCADE înseamnă că dacă un user e șters, i se șterg și vehiculele.
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vehicles'
    )

    # --- Detalii Vehicul ---
    make = models.CharField(max_length=100, verbose_name="Marcă") # ex: Volkswagen
    model = models.CharField(max_length=100, verbose_name="Model") # ex: Golf
    year = models.PositiveIntegerField(verbose_name="An fabricație") # ex: 2018

    # Numărul de înmatriculare este un identificator bun
    license_plate = models.CharField(
        max_length=20, 
        verbose_name="Număr înmatriculare",
        unique=True, # Previne adăugarea aceleiași mașini de două ori
        blank=True,  # Permite să fie gol dacă utilizatorul nu vrea să-l adauge
        null=True
    )

    # --- Informații Adiționale ---
    vin = models.CharField(
        max_length=17, 
        verbose_name="Serie șasiu (VIN)", 
        blank=True, # blank=True înseamnă că nu e obligatoriu în formular
        null=True
    )

    # Adăugăm datele de creare/modificare pentru o bună trasabilitate
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Aceasta este funcția care ne ajută să vedem un nume clar în admin
        # ex: "2018 Volkswagen Golf (DJ 01 ABC)"
        return f"{self.year} {self.make} {self.model} ({self.license_plate})"

    class Meta:
        # Setează cum să fie ordonate vehiculele când le cerem din baza de date
        ordering = ['-created_at'] # Cele mai noi prima dată
        # Asigură că un user nu poate adăuga 2 mașini cu același număr de înmatriculare
        unique_together = ('owner', 'license_plate')