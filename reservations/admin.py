from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("user","room","check_in","check_out","guests","total_price","status","created_at")
    list_filter = ("status",)
    search_fields = ("user__username","room__number")
