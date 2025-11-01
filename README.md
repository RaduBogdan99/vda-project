# Vehicle & Driver Assistant (VDA)

Minimal skeleton to start a Django + DRF project, with CI set up for lint and tests.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Initialize real Django project:
django-admin startproject vda_project vda_project
python vda_project/manage.py migrate
python vda_project/manage.py runserver
```
