from django import forms
from .models import Maintenance, MaintenanceAlert

class MaintenanceAlertForm(forms.ModelForm):
    class Meta:
        model = MaintenanceAlert
        # 'vehicle' va fi setat automat din view
        fields = [
            'description', 
            'km_interval', 
            'months_interval', 
            'last_performed_date', 
            'last_performed_odometer'
        ]

        widgets = {
            'last_performed_date': forms.DateInput(attrs={'type': 'date'}),
        }

        labels = {
            'description': 'Descriere Operațiune (ex: Schimb ulei)',
            'km_interval': 'Interval Kilometri (ex: 10000)',
            'months_interval': 'Interval Luni (ex: 12)',
            'last_performed_date': 'Data Ultimei Operațiuni',
            'last_performed_odometer': 'Kilometrajul la Ultima Operațiune'
        }

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