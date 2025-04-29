from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.api.views.allocation_details_views import AllocationDetailsViewSet

router = DefaultRouter()
router.register(r'', AllocationDetailsViewSet, basename='allocation-details')

urlpatterns = [
    path('', include(router.urls)),
]

