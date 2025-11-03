
# Create your views here.
from rest_framework import viewsets, permissions
from .models import Vehicle
from .serializers import VehicleSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    """
    API endpoint care permite utilizatorilor să vadă sau să editeze
    propriile vehicule.
    """
    serializer_class = VehicleSerializer
    # API-ul va fi accesibil doar utilizatorilor logați
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Această funcție este esențială.
        Restricționează API-ul să returneze DOAR vehiculele
        care aparțin utilizatorului care face cererea.
        """
        return Vehicle.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Setează automat proprietarul (owner) la utilizatorul logat
        atunci când se creează un vehicul nou prin API.
        """
        serializer.save(owner=self.request.user)