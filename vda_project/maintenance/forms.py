from django import forms
from .models import Maintenance

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        # 'vehicle' va fi setat automat din view
        fields = [
            'date', 
            'odometer', 
            'cost', 
            'notes', 
            'attachment'
        ]

        # Adăugăm widget-uri
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}), # O casetă de text mai mică
        }

        # Etichete
        labels = {
            'date': 'Data Operațiunii',
            'odometer': 'Kilometraj (km)',
            'cost': 'Cost (RON)',
            'notes': 'Descriere / Notițe',
            'attachment': 'Atașament (Factură)',
        }