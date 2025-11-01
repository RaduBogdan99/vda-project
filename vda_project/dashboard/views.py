from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from documents.models import Document


@login_required
def home(request):
    upcoming = Document.objects.filter(
        vehicle__owner=request.user, expires_on__lte=date.today() + timedelta(days=30)
    ).order_by("expires_on")
    return render(request, "dashboard/home.html", {"upcoming": upcoming})
