from rest_framework import serializers
from backend.api.models.tally_sessions import TallySession

class TallySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TallySession
        fields = '__all__'
        read_only_fields = ['id', 'date']




