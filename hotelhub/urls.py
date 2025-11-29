from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("accounts/", include("accounts.urls")),
    path("rooms/", include("rooms.urls")),
    path("reservations/", include("reservations.urls")),
    path("ai/", include("ai.urls")),  
]
