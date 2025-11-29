from django.contrib import admin
from .models import Room, Amenity

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("number","name","category","capacity","price_per_night","is_available")
    list_filter = ("category","is_available")
    search_fields = ("number","name","description")

admin.site.register(Amenity)
