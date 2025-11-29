from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rooms.models import Room
from reservations.models import Reservation

@login_required
def index(request):
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(is_available=True).count()
    pending = Reservation.objects.filter(status="PENDING").count()
    confirmed = Reservation.objects.filter(status="CONFIRMED").count()
    recent = Reservation.objects.select_related("room","user")[:10]
    return render(request, "dashboard.html", {
        "total_rooms": total_rooms,
        "available_rooms": available_rooms,
        "pending": pending,
        "confirmed": confirmed,
        "recent": recent,
    })
