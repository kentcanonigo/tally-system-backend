from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.api.views.weight_classifications_views import WeightClassificationViewSet

router = DefaultRouter()
router.register(r'', WeightClassificationViewSet, basename='weight-classifications')

urlpatterns = [
    path('', include(router.urls)),
]
