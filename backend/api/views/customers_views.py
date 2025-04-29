from rest_framework import viewsets
from backend.api.models.customers import Customer
from backend.api.serializers.customers_serializer import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
