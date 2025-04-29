from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.api.views.tally_sessions_views import TallySessionViewSet

router = DefaultRouter()
router.register(r'', TallySessionViewSet, basename='tally-sessions')

urlpatterns = [
    path('', include(router.urls)),
]

