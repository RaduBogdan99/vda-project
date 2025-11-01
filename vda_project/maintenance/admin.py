from django.contrib import admin

from .models import MaintenanceRecord


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "service_type", "date", "odometer_km", "cost")
    list_filter = ("service_type", "date")
    search_fields = ("vehicle__make", "vehicle__model", "vehicle__vin")
