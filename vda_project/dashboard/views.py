from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.decorators import login_required
from vehicles.models import Vehicle
from vehicles.forms import VehicleForm
from django.contrib import messages
from documents.models import Document
from documents.forms import DocumentForm      
from maintenance.models import Maintenance
from django.db.models import Sum  
from maintenance.forms import MaintenanceForm
import csv 
from django.http import HttpResponse 

@login_required 
def dashboard_view(request):
    # 1. Luăm toate vehiculele din baza de date
    all_vehicles = Vehicle.objects.all()

    # 2. Filtrăm lista pentru a păstra DOAR vehiculele
    #    unde "owner" este utilizatorul logat (request.user)
    user_vehicles = all_vehicles.filter(owner=request.user)

    # 3. Pregătim contextul pentru a-l trimite la HTML
    context = {
        'vehicle_list': user_vehicles,
    }

    # 4. Afișăm pagina HTML și îi trimitem lista de vehicule
    return render(request, 'dashboard/main.html', context)


@login_required
def vehicle_create_view(request):
    if request.method == 'POST':
        # Dacă formularul este trimis, îl procesăm
        form = VehicleForm(request.POST)
        if form.is_valid():
            # Formularul e valid, dar nu-l salvăm încă
            vehicle = form.save(commit=False)

            # Aici setăm proprietarul!
            vehicle.owner = request.user 

            # Acum salvăm vehiculul în baza de date
            vehicle.save()

            # Adăugăm un mesaj de succes
            messages.success(request, 'Vehiculul a fost adăugat cu succes!')

            # Redirecționăm utilizatorul înapoi la dashboard
            return redirect('dashboard:main')
    else:
        # Dacă e o cerere GET, afișăm formularul gol
        form = VehicleForm()

    context = {
        'form': form
    }
    return render(request, 'dashboard/vehicle_form.html', context)

@login_required
def vehicle_detail_view(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, owner=request.user)

    # 2. Găsește documentele DOAR pentru acest vehicul
    # Folosim .filter() pe modelul Document
    documents = Document.objects.filter(vehicle=vehicle)

    # 3. Găsește înregistrările de mentenanță DOAR pentru acest vehicul
    maintenance_records = Maintenance.objects.filter(vehicle=vehicle)
    total_maintenance_cost = maintenance_records.aggregate(total=Sum('cost'))['total'] or 0.00

    # 4. Trimite totul la template
    context = {
        'vehicle': vehicle,
        'documents': documents,
        'maintenance_records': maintenance_records,
        'total_maintenance_cost': total_maintenance_cost,
    }
    return render(request, 'dashboard/vehicle_detail.html', context)

@login_required
def document_create_view(request, vehicle_pk):
    # 1. Găsim vehiculul de care aparține documentul
    # Ne asigurăm că vehiculul este al utilizatorului logat
    vehicle = get_object_or_404(Vehicle, pk=vehicle_pk, owner=request.user)

    if request.method == 'POST':
        # request.FILES este necesar pentru a prelua fișierele (atașamentele)
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            # 2. Setăm câmpul 'vehicle' manual
            doc.vehicle = vehicle
            doc.save()

            messages.success(request, f'Documentul "{doc.get_document_type_display()}" a fost adăugat.')
            # 3. Redirecționăm înapoi la pagina de detalii a vehiculului
            return redirect('dashboard:vehicle_detail', pk=vehicle.pk)
    else:
        form = DocumentForm()

    context = {
        'form': form,
        'vehicle': vehicle
    }
    return render(request, 'dashboard/document_form.html', context)

@login_required
def vehicle_delete_view(request, pk):
    # 1. Găsim vehiculul, asigurându-ne că aparține utilizatorului logat
    vehicle = get_object_or_404(Vehicle, pk=pk, owner=request.user)

    if request.method == 'POST':
        # Dacă formularul de confirmare este trimis (POST)...
        # Ștergem vehiculul
        vehicle.delete()

        # Adăugăm un mesaj de succes
        messages.success(request, f'Vehiculul "{vehicle.make} {vehicle.model}" a fost șters.')

        # Redirecționăm la dashboard-ul principal
        return redirect('dashboard:main')

    # Dacă este o cerere GET, afișăm pagina de confirmare
    context = {
        'vehicle': vehicle
    }
    return render(request, 'dashboard/vehicle_confirm_delete.html', context)

@login_required
def document_delete_view(request, vehicle_pk, pk):
    # 1. Găsim documentul. Folosim o interogare sigură:
    # Găsește documentul cu id=pk
    # ȘI asigură-te că aparține vehiculului cu id=vehicle_pk
    # ȘI asigură-te că acel vehicul aparține utilizatorului logat
    document = get_object_or_404(
        Document, 
        pk=pk, 
        vehicle__pk=vehicle_pk, 
        vehicle__owner=request.user
    )

    if request.method == 'POST':
        # Dacă formularul de confirmare este trimis (POST)...
        document_name = document.get_document_type_display()
        document.delete()

        messages.success(request, f'Documentul "{document_name}" a fost șters.')

        # Redirecționăm înapoi la pagina de detalii a vehiculului
        return redirect('dashboard:vehicle_detail', pk=vehicle_pk)

    
    context = {
        'document': document,
        'vehicle': document.vehicle # Trimitem și vehiculul pentru link-ul "Anulează"
    }
    return render(request, 'dashboard/document_confirm_delete.html', context)
@login_required
def document_edit_view(request, vehicle_pk, pk):
    # 1. Găsim documentul exact (folosind aceeași logică sigură)
    document = get_object_or_404(
        Document, 
        pk=pk, 
        vehicle__pk=vehicle_pk, 
        vehicle__owner=request.user
    )

    if request.method == 'POST':
        # 2. Populăm formularul cu datele trimise (request.POST)
        #    ȘI cu instanța documentului pe care îl edităm (instance=document)
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save() # Salvăm modificările
            messages.success(request, 'Documentul a fost actualizat cu succes.')
            # 3. Redirecționăm înapoi la pagina de detalii a vehiculului
            return redirect('dashboard:vehicle_detail', pk=vehicle_pk)
    else:
        # 4. Dacă e GET, creăm formularul și îl pre-populăm
        #    cu datele documentului existent (instance=document)
        #
        # ACEASTA ESTE LINIA CARE AVEA PROBABIL EROAREA
        form = DocumentForm(instance=document)

    context = {
        'form': form,
        'vehicle': document.vehicle
    }
    # 5. Refolosim același template ca la creare!
    return render(request, 'dashboard/document_form.html', context)
@login_required
def maintenance_create_view(request, vehicle_pk):
    # 1. Găsim vehiculul
    vehicle = get_object_or_404(Vehicle, pk=vehicle_pk, owner=request.user)

    if request.method == 'POST':
        form = MaintenanceForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            # 2. Setăm vehiculul manual
            record.vehicle = vehicle
            record.save()

            messages.success(request, 'Operațiunea de mentenanță a fost adăugată.')
            # 3. Redirecționăm înapoi la detalii
            return redirect('dashboard:vehicle_detail', pk=vehicle.pk)
    else:
        form = MaintenanceForm()

    context = {
        'form': form,
        'vehicle': vehicle
    }
    return render(request, 'dashboard/maintenance_form.html', context)
@login_required
def maintenance_edit_view(request, vehicle_pk, pk):
    # Găsim înregistrarea de mentenanță
    record = get_object_or_404(
        Maintenance, 
        pk=pk, 
        vehicle__pk=vehicle_pk, 
        vehicle__owner=request.user
    )

    if request.method == 'POST':
        # Populăm formularul cu datele noi și instanța existentă
        form = MaintenanceForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operațiunea de mentenanță a fost actualizată.')
            return redirect('dashboard:vehicle_detail', pk=vehicle_pk)
    else:
        # Afișăm formularul pre-populat cu datele existente
        form = MaintenanceForm(instance=record)

    context = {
        'form': form,
        'vehicle': record.vehicle
    }
    # Refolosim același template ca la creare
    return render(request, 'dashboard/maintenance_form.html', context)
@login_required
def maintenance_delete_view(request, vehicle_pk, pk):
    # Găsim înregistrarea
    record = get_object_or_404(
        Maintenance, 
        pk=pk, 
        vehicle__pk=vehicle_pk, 
        vehicle__owner=request.user
    )

    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Operațiunea de mentenanță a fost ștearsă.')
        return redirect('dashboard:vehicle_detail', pk=vehicle_pk)

    # Afișăm pagina de confirmare
    context = {
        'record': record,
        'vehicle': record.vehicle
    }
    return render(request, 'dashboard/maintenance_confirm_delete.html', context)

@login_required
def vehicle_edit_view(request, pk):
    # 1. Găsim vehiculul
    vehicle = get_object_or_404(Vehicle, pk=pk, owner=request.user)

    if request.method == 'POST':
        # 2. Populăm formularul cu datele noi (request.POST) și instanța veche
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehiculul a fost actualizat cu succes.')
            # 3. Redirecționăm înapoi la pagina de detalii
            return redirect('dashboard:vehicle_detail', pk=vehicle.pk)
    else:
        # 4. Afișăm formularul pre-populat cu datele vehiculului
        form = VehicleForm(instance=vehicle)

    context = {
        'form': form,
        'vehicle': vehicle
    }
    # 5. Refolosim același template ca la creare!
    return render(request, 'dashboard/vehicle_form.html', context)

@login_required
def export_maintenance_csv(request):
    # 1. Setează numele fișierului și tipul de răspuns
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="export_mentenanta_vda.csv"'},
    )

    # 2. Creează un "scriitor" CSV
    writer = csv.writer(response)

    # 3. Scrie antetul (capul de tabel)
    writer.writerow([
        'Data', 
        'Vehicul (Marca)', 
        'Vehicul (Model)', 
        'Vehicul (Nr. Inmatriculare)', 
        'Kilometraj', 
        'Cost (RON)', 
        'Notite'
    ])

    # 4. Găsește toate înregistrările de mentenanță ale utilizatorului
    records = Maintenance.objects.filter(vehicle__owner=request.user).order_by('date')

    # 5. Scrie fiecare rând în fișier
    for record in records:
        writer.writerow([
            record.date,
            record.vehicle.make,
            record.vehicle.model,
            record.vehicle.license_plate,
            record.odometer,
            record.cost,
            record.notes
        ])

    # 6. Returnează fișierul
    return response