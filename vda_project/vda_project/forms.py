from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User # <-- Importă User

class CustomUserCreationForm(UserCreationForm):
    # ... (codul tău existent) ...
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class UserProfileForm(forms.ModelForm):
    """
    Un formular simplu pentru a edita datele de bază ale utilizatorului.
    """
    class Meta:
        model = User
        # Câmpurile pe care le permitem la editare
        fields = ['first_name', 'last_name', 'email']
        # Etichete mai prietenoase
        labels = {
            'first_name': 'Prenume',
            'last_name': 'Nume',
            'email': 'Adresă de Email'
        }

class AdminUserEditForm(forms.ModelForm):
    """
    Un formular pentru admini pentru a edita detaliile de bază
    și permisiunile unui utilizator.
    """
    class Meta:
        model = User
        # Câmpurile pe care le poate edita un admin
        fields = [
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'is_active',  # Poate activa/dezactiva contul
            'is_staff',   # Poate face pe cineva "staff" (să intre în /admin/)
            'is_superuser' # Poate face pe cineva super-admin
        ]
        labels = {
            'is_active': 'Cont Activ',
            'is_staff': 'Permisiuni Staff (pentru /admin/)',
            'is_superuser': 'Permisiuni de Super-Admin'
        }