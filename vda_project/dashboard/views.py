from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from vda_project.forms import AdminUserEditForm
from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponse
import csv
from django.contrib.auth.models import User

# Importuri Modele
from vehicles.models import Vehicle
from documents.models import Document
from maintenance.models import Maintenance, MaintenanceAlert

# Importuri Formulare
from vehicles.forms import VehicleForm, VehicleOdometerForm
from documents.forms import DocumentForm
from maintenance.forms import MaintenanceForm, MaintenanceAlertForm


# --- Dashboard View ---
@login_required
def dashboard_view(request):
    user_vehicles = Vehicle.objects.filter(owner=request.user)
    context = {
        "vehicle_list": user_vehicles,
    }
    return render(request, "dashboard/main.html", context)


# --- Vehicle CRUD ---
@login_required
def vehicle_create_view(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            messages.success(request, "Vehiculul a fost adăugat cu succes!")
            return redirect("dashboard:main")
    else:
        form = VehicleForm()
    context = {"form": form}
    return render(request, "dashboard/vehicle_form.html", context)


@login_required
def vehicle_detail_view(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, owner=request.user)
    odometer_form = VehicleOdometerForm(instance=vehicle)

    if request.method == "POST":
        if "update_odometer" in request.POST:
            odometer_form = VehicleOdometerForm(request.POST, instance=vehicle)
            if odometer_form.is_valid():
                odometer_form.save()
                messages.success(request, "Kilometrajul a fost actualizat.")
                return redirect("dashboard:vehicle_detail", pk=vehicle.pk)

    documents = Document.objects.filter(vehicle=vehicle)
    maintenance_records = Maintenance.objects.filter(vehicle=vehicle)
    total_maintenance_cost = maintenance_records.aggregate(total=Sum("cost"))["total"] or 0.00
    maintenance_alerts = MaintenanceAlert.objects.filter(vehicle=vehicle)

    context = {
        "vehicle": vehicle,
        "documents": documents,
        "maintenance_records": maintenance_records,
        "total_maintenance_cost": total_maintenance_cost,
        "odometer_form": odometer_form,
        "maintenance_alerts": maintenance_alerts,
    }
    return render(request, "dashboard/vehicle_detail.html", context)


@login_required
def vehicle_edit_view(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, owner=request.user)
    if request.method == "POST":
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehiculul a fost actualizat cu succes.")
            return redirect("dashboard:vehicle_detail", pk=vehicle.pk)
    else:
        form = VehicleForm(instance=vehicle)
    context = {"form": form, "vehicle": vehicle}
    return render(request, "dashboard/vehicle_form.html", context)


@login_required
def vehicle_delete_view(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, owner=request.user)
    if request.method == "POST":
        vehicle.delete()
        messages.success(request, f'Vehiculul "{vehicle.make} {vehicle.model}" a fost șters.')
        return redirect("dashboard:main")
    context = {"vehicle": vehicle}
    return render(request, "dashboard/vehicle_confirm_delete.html", context)


# --- Document CRUD ---
@login_required
def document_create_view(request, vehicle_pk):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_pk, owner=request.user)
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.vehicle = vehicle
            doc.save()
            messages.success(
                request, f'Documentul "{doc.get_document_type_display()}" a fost adăugat.'
            )
            return redirect("dashboard:vehicle_detail", pk=vehicle.pk)
    else:
        form = DocumentForm()
    context = {"form": form, "vehicle": vehicle}
    return render(request, "dashboard/document_form.html", context)


@login_required
def document_edit_view(request, vehicle_pk, pk):
    document = get_object_or_404(
        Document, pk=pk, vehicle__pk=vehicle_pk, vehicle__owner=request.user
    )
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, "Documentul a fost actualizat cu succes.")
            return redirect("dashboard:vehicle_detail", pk=vehicle_pk)
    else:
        form = DocumentForm(instance=document)
    context = {"form": form, "vehicle": document.vehicle}
    return render(request, "dashboard/document_form.html", context)


@login_required
def document_delete_view(request, vehicle_pk, pk):
    document = get_object_or_404(
        Document, pk=pk, vehicle__pk=vehicle_pk, vehicle__owner=request.user
    )
    if request.method == "POST":
        document_name = document.get_document_type_display()
        document.delete()
        messages.success(request, f'Documentul "{document_name}" a fost șters.')
        return redirect("dashboard:vehicle_detail", pk=vehicle_pk)
    context = {"document": document, "vehicle": document.vehicle}
    return render(request, "dashboard/document_confirm_delete.html", context)


# --- Maintenance Record CRUD ---
@login_required
def maintenance_create_view(request, vehicle_pk):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_pk, owner=request.user)
    if request.method == "POST":
        form = MaintenanceForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.vehicle = vehicle
            record.save()
            messages.success(request, "Operațiunea de mentenanță a fost adăugată.")
            return redirect("dashboard:vehicle_detail", pk=vehicle.pk)
    else:
        form = MaintenanceForm()
    context = {"form": form, "vehicle": vehicle}
    return render(request, "dashboard/maintenance_form.html", context)


@login_required
def maintenance_edit_view(request, vehicle_pk, pk):
    record = get_object_or_404(
        Maintenance, pk=pk, vehicle__pk=vehicle_pk, vehicle__owner=request.user
    )
    if request.method == "POST":
        form = MaintenanceForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Operațiunea de mentenanță a fost actualizată.")
            return redirect("dashboard:vehicle_detail", pk=vehicle_pk)
    else:
        form = MaintenanceForm(instance=record)
    context = {"form": form, "vehicle": record.vehicle}
    return render(request, "dashboard/maintenance_form.html", context)


@login_required
def maintenance_delete_view(request, vehicle_pk, pk):
    record = get_object_or_404(
        Maintenance, pk=pk, vehicle__pk=vehicle_pk, vehicle__owner=request.user
    )
    if request.method == "POST":
        record.delete()
        messages.success(request, "Operațiunea de mentenanță a fost ștearsă.")
        return redirect("dashboard:vehicle_detail", pk=vehicle_pk)
    context = {"record": record, "vehicle": record.vehicle}
    return render(request, "dashboard/maintenance_confirm_delete.html", context)


# --- Maintenance Alert CRUD ---
@login_required
def maintenance_alert_create_view(request, vehicle_pk):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_pk, owner=request.user)
    if request.method == "POST":
        form = MaintenanceAlertForm(request.POST)
        if form.is_valid():
            alert = form.save(commit=False)
            alert.vehicle = vehicle
            alert.save()
            messages.success(request, "Regula de alertă a fost adăugată.")
            return redirect("dashboard:vehicle_detail", pk=vehicle.pk)
    else:
        form = MaintenanceAlertForm()
    context = {"form": form, "vehicle": vehicle}
    return render(request, "dashboard/maintenance_alert_form.html", context)


@login_required
def maintenance_alert_edit_view(request, vehicle_pk, pk):
    alert = get_object_or_404(
        MaintenanceAlert, pk=pk, vehicle__pk=vehicle_pk, vehicle__owner=request.user
    )
    if request.method == "POST":
        form = MaintenanceAlertForm(request.POST, instance=alert)
        if form.is_valid():
            form.save()
            messages.success(request, "Regula de alertă a fost actualizată.")
            return redirect("dashboard:vehicle_detail", pk=vehicle_pk)
    else:
        form = MaintenanceAlertForm(instance=alert)
    context = {"form": form, "vehicle": alert.vehicle}
    return render(request, "dashboard/maintenance_alert_form.html", context)


@login_required
def maintenance_alert_delete_view(request, vehicle_pk, pk):
    alert = get_object_or_404(
        MaintenanceAlert, pk=pk, vehicle__pk=vehicle_pk, vehicle__owner=request.user
    )
    if request.method == "POST":
        alert.delete()
        messages.success(request, "Regula de alertă a fost ștearsă.")
        return redirect("dashboard:vehicle_detail", pk=vehicle_pk)
    context = {"alert": alert, "vehicle": alert.vehicle}
    return render(request, "dashboard/maintenance_alert_confirm_delete.html", context)


# --- Export CSV ---
@login_required
def export_maintenance_csv(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="export_mentenanta_vda.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(
        [
            "Data",
            "Vehicul (Marca)",
            "Vehicul (Model)",
            "Vehicul (Nr. Inmatriculare)",
            "Kilometraj",
            "Cost (RON)",
            "Notite",
        ]
    )
    records = Maintenance.objects.filter(vehicle__owner=request.user).order_by("date")
    for record in records:
        writer.writerow(
            [
                record.date,
                record.vehicle.make,
                record.vehicle.model,
                record.vehicle.license_plate,
                record.odometer,
                record.cost,
                record.notes,
            ]
        )
    return response


# Funcție helper care verifică dacă un user este admin
def is_admin(user):
    return user.is_superuser


@login_required
@user_passes_test(is_admin)  # <-- Acest decorator blochează accesul non-adminilor
def admin_dashboard_view(request):
    # 1. Colectăm statistici globale
    total_users = User.objects.count()
    total_vehicles = Vehicle.objects.count()
    total_documents = Document.objects.count()
    total_maintenance = Maintenance.objects.count()

    # 2. Colectăm date recente
    recent_users = User.objects.order_by("-date_joined")[:5]  # Ultimii 5 useri înregistrați

    context = {
        "total_users": total_users,
        "total_vehicles": total_vehicles,
        "total_documents": total_documents,
        "total_maintenance": total_maintenance,
        "recent_users": recent_users,
    }

    # Trimitem la un template NOU
    return render(request, "dashboard/admin_dashboard.html", context)


@login_required
@user_passes_test(is_admin)  # Asigură-te că doar adminii accesează
def admin_user_edit_view(request, pk):
    # Găsim utilizatorul pe care vrem să-l edităm
    user_to_edit = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        form = AdminUserEditForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            form.save()
            messages.success(request, f"Profilul lui {user_to_edit.username} a fost actualizat.")
            return redirect("dashboard:admin_dashboard")  # Trimite înapoi la panoul admin
    else:
        # Afișează formularul pre-completat cu datele utilizatorului
        form = AdminUserEditForm(instance=user_to_edit)

    context = {"form": form, "user_to_edit": user_to_edit}
    return render(request, "dashboard/admin_user_edit.html", context)


@login_required
@user_passes_test(is_admin)  # Asigură-te că doar adminii accesează
def admin_user_delete_view(request, pk):
    # Găsim utilizatorul pe care vrem să-l ștergem
    user_to_delete = get_object_or_404(User, pk=pk)

    # O măsură de siguranță: nu lăsa un admin să-și șteargă propriul cont
    if request.user == user_to_delete:
        messages.error(request, "Nu îți poți șterge propriul cont de admin de aici.")
        return redirect("dashboard:admin_dashboard")

    if request.method == "POST":
        username = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f'Utilizatorul "{username}" a fost șters cu succes.')
        return redirect("dashboard:admin_dashboard")

    context = {"user_to_delete": user_to_delete}
    return render(request, "dashboard/admin_user_confirm_delete.html", context)
