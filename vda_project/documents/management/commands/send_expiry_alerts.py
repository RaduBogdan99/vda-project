from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from documents.models import Document
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Trimite alerte prin e-mail pentru documentele care expira curand.'

    def handle(self, *args, **options):
        # Afișăm un mesaj în consolă că scriptul a pornit
        self.stdout.write(self.style.SUCCESS('Se porneste scriptul de alerte...'))
        
        today = timezone.now().date()
        
        # Definim perioadele de alertă (ex: 7 zile și 30 de zile)
        alert_periods = [7, 30]
        
        # Găsim toți utilizatorii care au cel puțin un document
        users_with_documents = User.objects.filter(
            vehicles__documents__isnull=False
        ).distinct()

        total_emails_sent = 0

        for user in users_with_documents:
            expiring_soon = []
            
            # Verificăm fiecare perioadă de alertă
            for days in alert_periods:
                target_date = today + timedelta(days=days)
                
                # Căutăm documente care expiră EXACT în acea zi
                documents = Document.objects.filter(
                    vehicle__owner=user,
                    expiry_date=target_date
                )
                
                for doc in documents:
                    expiring_soon.append(
                        f"- {doc.get_document_type_display()} "
                        f"pentru {doc.vehicle.make} {doc.vehicle.model} "
                        f"expiră în {days} zile (pe {doc.expiry_date})."
                    )

            # Dacă am găsit documente care expiră pentru acest utilizator
            if expiring_soon:
                # Construim mesajul e-mail-ului
                subject = '[VDA] Alerte de expirare documente'
                
                message_body = (
                    f"Salut, {user.username}!\n\n"
                    "Acesta este un memento automat de la Asistentul tau VDA.\n"
                    "Următoarele documente necesită atenția ta:\n\n"
                )
                
                message_body += "\n".join(expiring_soon)
                
                message_body += (
                    "\n\nTe rugăm să te loghezi în aplicație pentru a le actualiza."
                    "\n\nO zi bună!"
                )
                
                # Trimitem e-mail-ul
                try:
                    send_mail(
                        subject,
                        message_body,
                        settings.DEFAULT_FROM_EMAIL, # Expeditor (din settings.py)
                        [user.email],                # Destinatar
                        fail_silently=False,
                    )
                    self.stdout.write(self.style.SUCCESS(
                        f'Email de alerta trimis cu succes lui {user.username}'
                    ))
                    total_emails_sent += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f'Eroare la trimiterea email-ului către {user.username}: {e}'
                    ))

        self.stdout.write(self.style.SUCCESS(
            f'Scriptul a terminat. Total email-uri trimise: {total_emails_sent}'
        ))