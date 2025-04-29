from rest_framework import viewsets
from backend.api.models.tally_sessions import TallySession
from backend.api.serializers.tally_sessions_serializer import TallySessionSerializer

class TallySessionViewSet(viewsets.ModelViewSet):
    queryset = TallySession.objects.all()
    serializer_class = TallySessionSerializer
