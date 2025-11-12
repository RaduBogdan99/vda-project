from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Importuri pentru formularele de Autentificare
from .forms import CustomUserCreationForm, UserProfileForm

# Importuri pentru alertele din Home
from documents.models import Document
from maintenance.models import MaintenanceAlert
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta


def home_view(request):
    context = {}

    if request.user.is_authenticated:
        today = timezone.now().date()
        alert_period = today + timedelta(days=7)

        # --- 1. Logica pentru ALERTE DOCUMENTE (MODIFICATĂ) ---
        expiring_documents_qs = Document.objects.filter(
            vehicle__owner=request.user, expiry_date__lte=alert_period
        ).order_by("expiry_date")

        expiring_documents_list = []
        for doc in expiring_documents_qs:
            days_remaining = (doc.expiry_date - today).days
            expiring_documents_list.append(
                {
                    "doc": doc,
                    "days_remaining": days_remaining,
                    "days_abs": abs(days_remaining),  # <-- AM ADĂUGAT VALOAREA ABSOLUTĂ AICI
                }
            )

        context["expiring_documents"] = expiring_documents_list

        # --- 2. Logica pentru ALERTE MENTENANȚĂ (Neschimbată) ---
        due_maintenance = []
        all_alerts = MaintenanceAlert.objects.filter(vehicle__owner=request.user)

        for alert in all_alerts:
            is_due = False
            due_reason = ""

            # Verifică alerta de KM
            if alert.km_interval and alert.km_interval > 0:
                due_km = alert.last_performed_odometer + alert.km_interval
                km_remaining = due_km - alert.vehicle.current_odometer

                if km_remaining <= 500:
                    is_due = True
                    if km_remaining >= 0:
                        due_reason = f"Mai sunt {km_remaining} km pana la revizie"
                    else:
                        due_reason = f"Revizie depasita cu {abs(km_remaining)} km!"

            # Verifică alerta de Timp
            if not is_due and alert.months_interval and alert.months_interval > 0:
                due_date = alert.last_performed_date + relativedelta(months=alert.months_interval)
                days_remaining_rel = (due_date - today).days

                if days_remaining_rel <= 7:
                    is_due = True
                    if days_remaining_rel >= 0:
                        due_reason = f"Revizie necesara in {days_remaining_rel} zile"
                    else:
                        due_reason = f"Revizie depasita cu {abs(days_remaining_rel)} zile!"

            if is_due:
                due_maintenance.append({"alert": alert, "reason": due_reason})

        context["due_maintenance"] = due_maintenance

    return render(request, "home.html", context)


# --- FUNCȚIA CARE LIPSEA ---
def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


# --- FUNCȚIA CARE LIPSEA ---
@login_required
def profile_settings_view(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profilul tău a fost actualizat cu succes!")
            return redirect("profile_settings")
    else:
        form = UserProfileForm(instance=request.user)

    context = {"form": form}
    return render(request, "accounts/profile_settings.html", context)
