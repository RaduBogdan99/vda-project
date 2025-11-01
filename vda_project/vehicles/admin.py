from django.contrib import admin

from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("owner", "make", "model", "year", "vin", "created_at")
    search_fields = ("make", "model", "vin", "owner__username")
    list_filter = ("year",)
