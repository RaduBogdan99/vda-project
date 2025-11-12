from django.contrib import admin
from .models import Maintenance  # <-- Numele corect este Maintenance


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    # Ce coloane să afișăm în listă
    list_display = ("vehicle", "date", "odometer", "cost", "notes")

    # Filtre utile în dreapta
    list_filter = ("date", "vehicle__make")

    # Căutare
    search_fields = ("vehicle__license_plate", "notes")
