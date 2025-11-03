from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        # Specificăm ce câmpuri din model să apară în formular
        # "owner" (proprietarul) va fi setat automat din view,
        # deci nu trebuie să-l punem aici.
        fields = ['make', 'model', 'year', 'license_plate', 'vin']

        # Opțional: adăugăm niște etichete mai prietenoase
        labels = {
            'make': 'Marcă',
            'model': 'Model',
            'year': 'An fabricație',
            'license_plate': 'Număr înmatriculare',
            'vin': 'Serie șasiu (VIN)',
        }