from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        # Câmpurile pe care le vrem în formular
        # 'vehicle' va fi setat automat din view
        fields = ["document_type", "issue_date", "expiry_date", "notes", "attachment"]

        # Adăugăm "widgets" pentru a face câmpurile de dată interactive
        widgets = {
            "issue_date": forms.DateInput(attrs={"type": "date"}),
            "expiry_date": forms.DateInput(attrs={"type": "date"}),
        }

        # Etichete
        labels = {
            "document_type": "Tip Document",
            "issue_date": "Data Emiterii",
            "expiry_date": "Data Expirării",
            "notes": "Notițe",
            "attachment": "Atașament (PDF/Poză)",
        }
