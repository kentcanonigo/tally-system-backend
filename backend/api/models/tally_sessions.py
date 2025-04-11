from django.db import models
from .customers import Customer
from .plants import Plant

class TallySession(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.TextField()

    def __str__(self):
        return f"Session {self.id} - {self.customer.name} at {self.plant.name}"
