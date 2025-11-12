from rest_framework import viewsets, permissions
from .models import Document
from .serializers import DocumentSerializer
from vehicles.models import Vehicle  # Avem nevoie de el pentru a filtra


class DocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint care permite utilizatorilor să vadă sau să editeze
    propriile documente.
    """

    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Returnează DOAR documentele care aparțin vehiculelor
        utilizatorului logat.
        """
        return Document.objects.filter(vehicle__owner=self.request.user)

    def get_serializer(self, *args, **kwargs):
        """
        Modifică serializer-ul pentru a filtra câmpul 'vehicle'
        astfel încât să arate doar vehiculele utilizatorului curent
        atunci când creează/editează un document.
        """
        serializer = super().get_serializer(*args, **kwargs)
        if self.request:
            # Filtrează queryset-ul pentru câmpul 'vehicle'
            serializer.fields["vehicle"].queryset = Vehicle.objects.filter(owner=self.request.user)
        return serializer

    # perform_create nu este necesar, deoarece 'vehicle' este trimis
    # direct în formularul API, iar filtrul de mai sus îl validează.
