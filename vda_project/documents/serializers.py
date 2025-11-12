from rest_framework import serializers
from .models import Document
from vehicles.models import Vehicle


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializer pentru modelul Document.
    """

    # Facem 'vehicle' un câmp editabil, dar care va fi filtrat
    # pentru a afișa doar vehiculele utilizatorului.
    vehicle = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all())

    # Afișăm numele tipului de document, nu doar codul (ex: "Asigurare RCA")
    document_type = serializers.CharField(source="get_document_type_display", read_only=True)

    class Meta:
        model = Document
        fields = [
            "id",
            "vehicle",
            "document_type",
            "issue_date",
            "expiry_date",
            "notes",
            "attachment",
            "created_at",
        ]
        read_only_fields = ["created_at"]
