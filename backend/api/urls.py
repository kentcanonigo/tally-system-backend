from django.urls import path, include

urlpatterns = [
    path("customers/", include("backend.api.urls.customers_urls")),
    path("plants/", include("backend.api.urls.plants_urls")),
    path("tally-sessions/", include("backend.api.urls.tally_sessions_urls")),
    path("allocations/", include("backend.api.urls.allocation_details_urls")),
    path("weight-classifications/", include("backend.api.urls.weight_classifications_urls")),
]