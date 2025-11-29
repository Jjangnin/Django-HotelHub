from django.db import models
from django.contrib.auth.models import User
from rooms.models import Room
from django.core.exceptions import ValidationError
from datetime import timedelta

class Reservation(models.Model):
    STATUS = [
        ("PENDING","대기"),
        ("CONFIRMED","확정"),
        ("CANCELLED","취소"),
        ("CHECKED_IN","체크인"),
        ("CHECKED_OUT","체크아웃"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservations")
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField(default=1)
    request_notes = models.TextField(blank=True)
    total_price = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.room} ({self.check_in}~{self.check_out})"

    @property
    def nights(self):
        return (self.check_out - self.check_in).days

    def clean(self):
        if self.check_in >= self.check_out:
            raise ValidationError("체크아웃 날짜가 체크인 이후여야 합니다.")
        if self.guests < 1:
            raise ValidationError("인원은 1명 이상이어야 합니다.")
        if self.guests > self.room.capacity:
            raise ValidationError(f"정원 초과입니다. (최대 {self.room.capacity}명)")
        # 겹치는 예약 방지 (대기/확정/체크인 상태와 겹치면 불가)
        overlap = Reservation.objects.filter(
            room=self.room,
            status__in=["PENDING","CONFIRMED","CHECKED_IN"],
        ).exclude(pk=self.pk).filter(
            check_in__lt=self.check_out, check_out__gt=self.check_in
        ).exists()
        if overlap:
            raise ValidationError("해당 날짜에 이미 예약이 있습니다.")

    def save(self, *args, **kwargs):
        # 총 가격 = 박수 × 1박요금
        self.total_price = max(self.nights, 0) * self.room.price_per_night
        super().save(*args, **kwargs)
