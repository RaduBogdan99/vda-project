from rest_framework import viewsets, permissions
from .models import Maintenance
from .serializers import MaintenanceSerializer
from vehicles.models import Vehicle


class MaintenanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint care permite utilizatorilor să vadă sau să editeze
    propriile înregistrări de mentenanță.
    """

    serializer_class = MaintenanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Returnează DOAR înregistrările care aparțin vehiculelor
        utilizatorului logat.
        """
        return Maintenance.objects.filter(vehicle__owner=self.request.user)

    def get_serializer(self, *args, **kwargs):
        """
        Filtrează câmpul 'vehicle' pentru a arăta doar
        vehiculele utilizatorului curent.
        """
        serializer = super().get_serializer(*args, **kwargs)
        if self.request:
            serializer.fields["vehicle"].queryset = Vehicle.objects.filter(owner=self.request.user)
        return serializer
