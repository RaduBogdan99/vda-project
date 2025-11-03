from rest_framework import serializers
from .models import Maintenance
from vehicles.models import Vehicle

class MaintenanceSerializer(serializers.ModelSerializer):
    """
    Serializer pentru modelul Maintenance.
    """
    vehicle = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all()
    )

    class Meta:
        model = Maintenance
        fields = [
            'id', 
            'vehicle', 
            'date', 
            'odometer', 
            'cost', 
            'notes', 
            'attachment', 
            'created_at'
        ]
        read_only_fields = ['created_at']