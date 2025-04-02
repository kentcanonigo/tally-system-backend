from django.db import models
from .plants import Plant

class WeightClassification(models.Model):
    id = models.AutoField(primary_key=True)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="weight_classes")
    classification = models.TextField()
    min_weight = models.FloatField()
    max_weight = models.FloatField()

    def __str__(self):
        return f"{self.classification} ({self.min_weight}-{self.max_weight} kg)"