from django.contrib import admin
from backend.api.models.customers import Customer

# Register your models here.
admin.site.register([
    Customer,
])