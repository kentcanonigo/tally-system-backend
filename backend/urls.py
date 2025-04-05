from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("backend.api.urls")),  # only point to the __init__.py in `urls/`
]
