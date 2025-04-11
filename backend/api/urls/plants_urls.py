from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.api.views.plants_views import PlantViewSet

router = DefaultRouter()
router.register(r'', PlantViewSet, basename='plants')

urlpatterns = [
    path('', include(router.urls)),
]
