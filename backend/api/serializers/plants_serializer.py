from rest_framework import serializers
from backend.api.models.plants import Plant

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'
        read_only_fields = ['id']




