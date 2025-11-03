from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm # Pentru signup

# Importurile necesare pentru home_view (alerte)
from documents.models import Document
from django.utils import timezone
from datetime import timedelta


def home_view(request):
    # Inițializăm un context gol
    context = {}

    # Verificăm dacă utilizatorul este logat
    if request.user.is_authenticated:
        # 1. Definim perioada de căutare
        today = timezone.now().date()
        alert_period = today + timedelta(days=30)

        # 2. Căutăm documentele care aparțin vehiculelor utilizatorului
        #    ȘI care expiră între ziua de azi ȘI următoarele 30 de zile
        expiring_documents = Document.objects.filter(
            vehicle__owner=request.user,  # Doar ale utilizatorului
            expiry_date__gte=today,       # Expiră de azi încolo
            expiry_date__lte=alert_period # Până în 30 de zile
        ).order_by('expiry_date') # Le ordonăm pe cele mai apropiate prima dată

        # 3. Adăugăm documentele găsite și data de azi în context
        context['expiring_documents'] = expiring_documents
        context['today'] = today

    # 4. Afișăm pagina HTML, trimițând datele (sau contextul gol dacă nu e logat)
    return render(request, 'home.html', context)


# ACEASTA ESTE FUNCȚIA CARE LIPSEA:
def signup_view(request):
    # Verifică dacă formularul a fost trimis (metoda POST)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Dacă formularul e valid, salvează utilizatorul în baza de date
            user = form.save()

            # Loghează automat utilizatorul nou creat
            login(request, user)

            # Redirecționează către pagina principală
            return redirect('home')
    else:
        # Dacă e o cerere GET, afișează formularul gol
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})