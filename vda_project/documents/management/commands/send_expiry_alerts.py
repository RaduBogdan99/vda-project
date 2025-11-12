from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from documents.models import Document
from maintenance.models import MaintenanceAlert
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta


class Command(BaseCommand):
    help = "Trimite alerte prin e-mail pentru documente si mentenanta."

    def handle(self, *args, **options):
        # Mesaje FĂRĂ diacritice pentru a evita eroarea 'charmap'
        self.stdout.write(self.style.SUCCESS("Se porneste scriptul de alerte..."))

        today = timezone.now().date()
        alert_period = today + timedelta(days=7)
        total_emails_sent = 0

        users = User.objects.filter(is_active=True).exclude(email__exact="")

        for user in users:
            alert_messages = []

            # --- 1. Verifică Documente (LOGICĂ CORECTATĂ) ---
            # Găsim TOATE documentele care au expirat sau expiră în 30 de zile
            documents_to_check = Document.objects.filter(
                vehicle__owner=user,
                expiry_date__lte=alert_period,  # Tot ce e mai vechi sau egal cu "peste 30 de zile"
            ).order_by("expiry_date")

            for doc in documents_to_check:
                days_remaining = (doc.expiry_date - today).days

                if days_remaining < 0:
                    # A expirat deja
                    alert_messages.append(
                        f"- DOCUMENT: {doc.get_document_type_display()} "
                        f"pentru {doc.vehicle.make} {doc.vehicle.model} "
                        f"A EXPIRAT pe {doc.expiry_date.strftime('%d-%m-%Y')}."
                    )
                elif days_remaining <= 30:
                    # Expiră în curând (în 30 de zile sau mai puțin)
                    alert_messages.append(
                        f"- DOCUMENT: {doc.get_document_type_display()} "
                        f"pentru {doc.vehicle.make} {doc.vehicle.model} "
                        f"expira in {days_remaining} zile (pe {doc.expiry_date.strftime('%d-%m-%Y')})."
                    )

            # --- 2. Verifică Mentenanța (Logica pe care o aveam) ---
            all_alerts = MaintenanceAlert.objects.filter(vehicle__owner=user)

            for alert in all_alerts:
                is_due = False
                due_reason = ""

                if alert.km_interval and alert.km_interval > 0:
                    due_km = alert.last_performed_odometer + alert.km_interval
                    km_remaining = due_km - alert.vehicle.current_odometer

                    if km_remaining <= 500:  # Alertă cu 500km înainte sau dacă e depășit
                        is_due = True
                        if km_remaining >= 0:
                            due_reason = f"mai sunt {km_remaining} km pana la revizie."
                        else:
                            due_reason = f"revizie depasita cu {abs(km_remaining)} km!"

                if not is_due and alert.months_interval and alert.months_interval > 0:
                    due_date = alert.last_performed_date + relativedelta(
                        months=alert.months_interval
                    )
                    days_remaining = (due_date - today).days

                    if days_remaining <= 7:  # Alertă cu 7 zile înainte
                        is_due = True
                        if days_remaining >= 0:
                            due_reason = f"revizie necesara in {days_remaining} zile."
                        else:
                            due_reason = f"revizie depasita cu {abs(days_remaining)} zile!"

                if is_due:
                    alert_messages.append(
                        f"- MENTENANTA: {alert.description} "
                        f"pentru {alert.vehicle.make} {alert.vehicle.model} "
                        f"trebuie efectuata ({due_reason})"
                    )

            # --- 3. Trimite E-mail-ul (dacă am găsit alerte) ---
            if alert_messages:
                subject = "[VDA] Alerte de expirare si mentenanta"
                message_body = (
                    f"Salut, {user.username}!\n\n"
                    "Acesta este un memento automat de la Asistentul tau VDA.\n"
                    "Urmatoarele elemente necesita atentia ta:\n\n"
                )
                message_body += "\n".join(alert_messages)
                message_body += (
                    "\n\nTe rugam sa te loghezi in aplicatie pentru a actualiza datele."
                    "\n\nO zi buna!"
                )

                try:
                    send_mail(
                        subject,
                        message_body,
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f"Email de alerta trimis cu succes lui {user.username}")
                    )
                    total_emails_sent += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Eroare la trimiterea email-ului catre {user.username}: {e}"
                        )
                    )

        self.stdout.write(
            self.style.SUCCESS(f"Scriptul a terminat. Total email-uri trimise: {total_emails_sent}")
        )
