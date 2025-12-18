# VDA - Vehicle & Driver Assistant

**Vehicle & Driver Assistant (VDA)** este o aplicație web full-stack dezvoltată pentru gestionarea completă a ciclului de viață al vehiculelor personale. Aplicația permite utilizatorilor să monitorizeze documentele (RCA, ITP, Rovinietă), să țină evidența istoricului de mentenanță și să primească alerte automate înainte de expirarea documentelor sau depășirea intervalelor de service.

## 🚀 Funcționalități Principale

* **Management Vehicule:** Adăugare, editare și vizualizare detalii vehicule (VIN, an fabricație, kilometraj curent).
* **Gestiune Documente:** Urmărirea valabilității documentelor (RCA, ITP, CASCO) cu highlight vizual pentru cele expirate.
* **Jurnal Service:** Înregistrarea costurilor și a operațiunilor de mentenanță (ex: schimb ulei, plăcuțe frână).
* **Alerte Inteligente:** Sistem de notificări bazat pe timp (zile rămase) și kilometraj.
* **Automatizare:** Trimiterea automată a alertelor prin e-mail folosind scripturi personalizate (Management Commands) și Task Scheduler.
* **API RESTful:** Expunerea datelor pentru integrări externe, documentat prin Swagger/OpenAPI.
* **Panou Administrare:** Interfață dedicată administratorilor pentru gestionarea utilizatorilor.

## 🛠️ Tehnologii Utilizate

* **Backend:** Python 3.12, Django 5.2
* **API:** Django REST Framework (DRF), drf-spectacular
* **Frontend:** HTML5, Bootstrap 5, Django Crispy Forms
* **Bază de date:** SQLite (Default pentru dezvoltare)
* **Calitate Cod (CI/CD):** Black (formatter), Ruff (linter), Pytest (testing)
* **Securitate:** Python-Decouple (pentru gestionarea variabilelor de mediu)

---

## ⚙️ Instalare și Configurare Locală

Urmează pașii de mai jos pentru a rula proiectul pe mașina locală.

### 1. Clonare repository

```bash
git clone [https://github.com/RaduBogdan99/vda-project.git](https://github.com/RaduBogdan99/vda-project.git)
cd vda-project
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

# Configurare Email (SMTP Gmail)
EMAIL_USER=adresa.ta@gmail.com
EMAIL_PASS=parola_ta_de_aplicatie_16_caractere

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

Accesează aplicația în browser:

    Homepage: http://127.0.0.1:8000/

    Documentație API (Swagger UI): http://127.0.0.1:8000/api/docs/

    Schema API (YAML): http://127.0.0.1:8000/api/schema/

🤖 Automatizare și Scripturi

Aplicația include un script personalizat pentru verificarea alertelor și trimiterea email-urilor.

Rulare manuală a scriptului:

python manage.py send_expiry_alerts

Acest script este configurat să ruleze automat în Windows Task Scheduler pentru a verifica zilnic statusul documentelor și al reviziilor.
✅ Testare și Code Quality

Proiectul folosește GitHub Actions pentru Integrare Continuă (CI). Pentru a rula verificările local:

# Formatare cod
black .

# Verificare erori (linting)
ruff check .

# Rulare teste unitare
pytest