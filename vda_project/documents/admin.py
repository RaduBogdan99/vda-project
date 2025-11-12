from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):  # Aici era greșeala mea (era admin.admin)
    # Ce coloane să afișăm în listă
    list_display = (
        "vehicle",
        "document_type",  # Numele corect (nu doc_type)
        "issue_date",
        "expiry_date",  # Numele corect (nu expires_on)
        "created_at",
    )

    # Filtre utile în dreapta
    list_filter = ("document_type", "expiry_date", "vehicle__make")

    # Căutare
    search_fields = ("vehicle__make", "vehicle__model", "vehicle__license_plate", "notes")
