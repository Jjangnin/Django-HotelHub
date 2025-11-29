from django import forms
from .models import Reservation
from rooms.models import Room

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["room", "check_in", "check_out", "guests", "request_notes"]
        widgets = {
            "check_in": forms.DateInput(attrs={"type": "date"}),
            "check_out": forms.DateInput(attrs={"type": "date"}),
            "request_notes": forms.Textarea(attrs={"rows":3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 예약가능한 방만 우선적으로 보이게 (불가도 보이려면 아래 줄 삭제)
        self.fields["room"].queryset = Room.objects.all().order_by("number")
