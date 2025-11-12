from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator


class CustomUserCreationForm(UserCreationForm):

    username_validator = UnicodeUsernameValidator()
    username = forms.CharField(
        label="Nume utilizator",
        validators=[username_validator, MinLengthValidator(6)],
        help_text="Minim 6 caractere. Sunt permise litere, cifre si caracterele speciale: @/./+/-/_.",
        error_messages={
            "min_length": "Numele de utilizator trebuie să aibă cel puțin 6 caractere.",
        },
    )

    email = forms.EmailField(required=True)

    password1 = forms.CharField(
        label="Parolă",
        widget=forms.PasswordInput,
        # AICI ESTE MODIFICAREA:
        # Adăugăm regulile de validare direct în textul de ajutor, folosind HTML
        help_text=(
            '<small class="form-text text-muted">'
            "Parola ta trebuie să respecte următoarele reguli:"
            "<ul>"
            "<li>Trebuie să conțină cel puțin 8 caractere.</li>"
            "<li>Nu poate fi prea similară cu informațiile tale personale (ex: nume utilizator).</li>"
            '<li>Nu poate fi o parolă comună (ex: "password123").</li>'
            "<li>Nu poate fi compusă doar din cifre.</li>"
            "</ul>"
            "</small>"
        ),
    )

    password2 = forms.CharField(
        label="Confirmare parolă",
        widget=forms.PasswordInput,
        help_text="Introdu aceeași parolă ca mai sus, pentru verificare.",
    )

    # --- SFÂRȘIT BLOC NOU ---

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
        fields = ["first_name", "last_name", "email"]
        # Etichete mai prietenoase
        labels = {"first_name": "Prenume", "last_name": "Nume", "email": "Adresă de Email"}


class AdminUserEditForm(forms.ModelForm):
    """
    Un formular pentru admini pentru a edita detaliile de bază
    și permisiunile unui utilizator.
    """

    class Meta:
        model = User
        # Câmpurile pe care le poate edita un admin
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",  # Poate activa/dezactiva contul
            "is_staff",  # Poate face pe cineva "staff" (să intre în /admin/)
            "is_superuser",  # Poate face pe cineva super-admin
        ]
        labels = {
            "is_active": "Cont Activ",
            "is_staff": "Permisiuni Staff (pentru /admin/)",
            "is_superuser": "Permisiuni de Super-Admin",
        }
