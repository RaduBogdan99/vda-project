from rest_framework import serializers
from .models import Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    """
    Serializer pentru modelul Vehicle.
    Expune toate câmpurile, dar face 'owner' read-only (doar citire).
    """

    # Afișăm numele proprietarului, nu doar ID-ul
    owner = serializers.StringRelatedField()

    class Meta:
        model = Vehicle
        # Listăm câmpurile pe care vrem să le expunem în API
        fields = [
            'id', 
            'owner', 
            'make', 
            'model', 
            'year', 
            'license_plate', 
            'vin', 
            'created_at', 
            'updated_at'
        ]
        # Setăm câmpurile care nu pot fi editate direct prin API
        read_only_fields = ['owner', 'created_at', 'updated_at']