from rest_framework import serializers
from backend.api.models.weight_classifications import WeightClassification

class WeightClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightClassification
        fields = '__all__'
        read_only_fields = ['id', 'classification', 'min_weight', 'max_weight']
    




