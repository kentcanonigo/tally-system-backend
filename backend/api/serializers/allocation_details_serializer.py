from rest_framework import serializers
from backend.api.models.allocation_details import AllocationDetails

class AllocationDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllocationDetails
        fields = '__all__'
        read_only_fields = ['id', 'allocation_id', 'tally_session_id', 'plant_id', 'customer_id', 'weight_classification_id']
    




