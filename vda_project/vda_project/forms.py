from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    # Adăugăm câmpul de email, pe care îl facem obligatoriu
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        # Folosim modelul de bază User
        model = User
        # Specificăm câmpurile care vor apărea pe formular
        # Adăugăm 'email' pe lângă 'username'
        fields = ("username", "email")