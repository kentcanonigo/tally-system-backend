from django.contrib import admin
from backend.api.models.customers import Customer
from backend.api.models.plants import Plant
from backend.api.models.weight_classifications import WeightClassification
from backend.api.models.tally_sessions import TallySession
from backend.api.models.allocation_details import AllocationDetails

# Register your models here.
admin.site.register([
    Customer,
    Plant,
    WeightClassification,
    TallySession,
    AllocationDetails,
])