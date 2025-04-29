from rest_framework import viewsets
from backend.api.models.plants import Plant
from backend.api.serializers.plants_serializer import PlantSerializer

class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer