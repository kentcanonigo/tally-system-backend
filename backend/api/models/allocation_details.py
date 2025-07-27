from django.db import models
from .tally_sessions import TallySession
from .weight_classifications import WeightClassification

class AllocationDetails(models.Model):
    id = models.AutoField(primary_key=True)
    tally_session = models.ForeignKey(TallySession, on_delete=models.CASCADE)
    weight_class = models.ForeignKey(WeightClassification, on_delete=models.CASCADE)
    required_bags = models.FloatField()
    allocated_bags = models.FloatField(null=True, blank=True)  # Allow null/blank

    def __str__(self):
        return f"Session {self.tally_session.id}: {self.weight_class.classification} ({self.allocated_bags}/{self.required_bags})"
