from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "doc_type", "expires_on", "created_at")
    list_filter = ("doc_type", "expires_on")
    search_fields = ("vehicle__make", "vehicle__model", "vehicle__vin")
