from rest_framework import viewsets
from backend.api.models.weight_classifications import WeightClassification
from backend.api.serializers.weight_classifications_serializer import WeightClassificationSerializer

class WeightClassificationViewSet(viewsets.ModelViewSet):
    queryset = WeightClassification.objects.all()
    serializer_class = WeightClassificationSerializer
    