# 🚗 VDA - Vehicle & Driver Assistant

**VDA (Vehicle & Driver Assistant)** este o aplicație web construită în Django, concepută pentru a ajuta șoferii să își gestioneze vehiculele, documentele cu dată de expirare (RCA, ITP, Rovinietă) și istoricul de mentenanță.

Aplicația oferă o interfață prietenoasă, un API RESTful pentru extinderi viitoare și un sistem automat de notificări prin e-mail pentru alertele de expirare.

Acest proiect a fost dezvoltat ca parte a disciplinei "Instrumente pentru Dezvoltarea Programelor", cu un accent deosebit pe **trasabilitatea** proiectului folosind un ciclu de viață modern de dezvoltare software (Git, GitHub Issues, Pull Requests, CI/CD).

---

## 🚀 Funcționalități Principale

### 1. Managementul Utilizatorilor
* Sistem complet de autentificare (Înregistrare, Login, Logout).
* Funcționalitate de "Resetare Parolă" prin e-mail.
* Paginile sunt securizate (utilizatorii nu pot vedea sau modifica datele altor utilizatori).

### 2. Dashboard & Alerte
* O pagină principală (Home) care afișează un sumar al documentelor care expiră în următoarele 30 de zile.
* Un Dashboard central unde utilizatorii își pot vedea toate vehiculele.

### 3. CRUD (Create, Read, Update, Delete)
Aplicația permite managementul complet pentru:
* **Vehicule:** Adăugare, editare și ștergere a vehiculelor personale.
* **Documente:** Adăugarea, editarea și ștergerea documentelor (RCA, ITP etc.) pentru fiecare vehicul, inclusiv încărcarea de atașamente (PDF/imagini).
* **Mentenanță:** Adăugarea, editarea și ștergerea înregistrărilor de service (cost, kilometraj, notițe).

### 4. Notificări Automate
* Un script (`management command`) care rulează automat (printr-un cron job / Task Scheduler).
* Scriptul scanează baza de date și trimite e-mail-uri de avertizare utilizatorilor ale căror documente urmează să expire.

### 5. API RESTful
* Un API securizat (necesită autentificare) care expune datele în format JSON.
* Endpoint-uri complete pentru CRUD pe Vehicule, Documente și Mentenanță.
* Documentație API generată automat folosind **Swagger (OpenAPI)**.

### 6. Export de Date
* Funcționalitate de export a tuturor înregistrărilor de mentenanță într-un fișier `.csv` pentru analiză în Excel.

---

## 🛠️ Tehnologii și Instrumente Folosite

| Categorie | Tehnologie/Instrument | Rol |
| :--- | :--- | :--- |
| **Backend** | **Python 3.11+**, **Django** | Logica aplicației, ORM, autentificare, admin. |
| **API** | **Django REST Framework (DRF)** | Crearea API-ului RESTful. |
| **Frontend** | **Django Templates**, **Bootstrap 5** | Construirea interfeței utilizatorului. |
| **Formulare** | **django-crispy-forms** | Stilizarea rapidă a formularelor cu Bootstrap. |
| **Bază de Date** | **SQLite** | Bază de date ușoară pentru dezvoltare. |
| **Notificări** | **Django Management Commands**, **Task Scheduler** | Rularea script-urilor automate de alerte. |
| **Configurare** | **python-decouple** | Gestionarea securizată a secretelor (parole, chei API). |
| **Documentație API**| **drf-spectacular** | Generarea automată a paginii Swagger UI. |
| **CI/CD** | **GitHub Actions** | Automatizarea testării și linting-ului. |
| **Calitatea Codului**| **Black**, **Ruff** | Formatare de cod și identificarea erorilor. |
| **Testare** | **Pytest** | Rularea testelor unitare. |

---

## 🏁 Cum se Rulează Local

### 1. Cerințe preliminare
* Python 3.11+
* Git

### 2. Clonarea Proiectului
```bash
git clone (https://github.com/RaduBogdan99/vda-project)
cd vda-project


python -m venv .venv

.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

(Asigură-te că ai python-decouple, djangorestframework, drf-spectacular, django-crispy-forms, crispy-bootstrap5 în fișierul requirements.txt)

5. Configurarea Mediului (.env)

    Mergi la folderul de configurare: cd vda_project

    Creează un fișier numit .env.

    Adaugă cheile pentru serverul de e-mail (ex: Gmail):
    Ini, TOML

    EMAIL_USER=adresa-ta-de-test@gmail.com
    EMAIL_PASS=parola-ta-de-aplicatie-de-16-caractere

6. Migrarea Bazei de Date

Întoarce-te la folderul manage.py (cd ..) și rulează:
Bash

python manage.py migrate

7. Crearea unui Super-Utilizator (Admin)

Bash

python manage.py createsuperuser

(Urmează instrucțiunile pentru a seta un nume de utilizator și o parolă)

8. Rularea Serverului

Bash

python manage.py runserver

Aplicația este acum disponibilă la http://127.0.0.1:8000/.

 Documentație API

Documentația API (Swagger UI) este generată automat și este disponibilă (după pornirea serverului) la adresa:

http://127.0.0.1:8000/api/docs/
