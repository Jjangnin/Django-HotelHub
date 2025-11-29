from django import forms
from .models import Room

class RoomFilterForm(forms.Form):
    q = forms.CharField(required=False, label="검색어")
    category = forms.ChoiceField(required=False, choices=[("", "전체")] + list(Room.CATEGORY_CHOICES), label="카테고리")
    status = forms.ChoiceField(required=False, choices=[("", "전체"), ("available","예약가능"), ("unavailable","예약불가")], label="상태")
