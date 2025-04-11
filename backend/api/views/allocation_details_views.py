from rest_framework import viewsets
from backend.api.models.allocation_details import AllocationDetails
from backend.api.serializers.allocation_details_serializer import AllocationDetailsSerializer

class AllocationDetailsViewSet(viewsets.ModelViewSet):
    queryset = AllocationDetails.objects.all()
    serializer_class = AllocationDetailsSerializer
