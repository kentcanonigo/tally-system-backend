from django.db import models

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()

    def __str__(self):
        return self.name
