from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Room
from .forms import RoomFilterForm

@login_required
def room_list(request):
    qs = Room.objects.all().order_by("number")
    form = RoomFilterForm(request.GET or None)
    if form.is_valid():
        q = form.cleaned_data.get("q")
        category = form.cleaned_data.get("category")
        status = form.cleaned_data.get("status")
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(number__icontains=q) | Q(description__icontains=q))
        if category:
            qs = qs.filter(category=category)
        if status == "available":
            qs = qs.filter(is_available=True)
        elif status == "unavailable":
            qs = qs.filter(is_available=False)
    return render(request, "rooms/list.html", {"form": form, "rooms": qs})

@login_required
def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, "rooms/detail.html", {"room": room})
