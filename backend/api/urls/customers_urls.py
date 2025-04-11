from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.api.views.customers_views import CustomerViewSet

router = DefaultRouter()
router.register(r'', CustomerViewSet, basename='customers')

urlpatterns = [
    path('', include(router.urls)),
]
