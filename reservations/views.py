from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Reservation
from .forms import ReservationForm

@login_required
def reservation_list(request):
    if request.user.is_staff:
        qs = Reservation.objects.select_related("user","room")
    else:
        qs = Reservation.objects.filter(user=request.user).select_related("room")
    # 템플릿의 상태 드롭다운에 사용
    status_choices = Reservation.STATUS
    return render(request, "reservations/list.html", {
        "reservations": qs,
        "status_choices": status_choices,
    })

@login_required
def reservation_create(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            res = form.save(commit=False)
            res.user = request.user
            try:
                res.full_clean()
                res.save()
                messages.success(request, "예약이 등록되었습니다.")
                return redirect("reservations:list")
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = ReservationForm()
    return render(request, "reservations/create.html", {"form": form})

def is_staff(user): return user.is_staff

@user_passes_test(is_staff)
def reservation_edit(request, pk):
    res = get_object_or_404(Reservation, pk=pk)
    if request.method == "POST":
        form = ReservationForm(request.POST, instance=res)
        if form.is_valid():
            res = form.save(commit=False)
            try:
                res.full_clean()
                res.save()
                messages.success(request, "예약이 수정되었습니다.")
                return redirect("reservations:list")
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = ReservationForm(instance=res)
    return render(request, "reservations/edit.html", {"form": form, "obj": res})

# ✅ 관리자만: 상태 변경 (POST)
@user_passes_test(is_staff)
def reservation_change_status(request, pk):
    res = get_object_or_404(Reservation, pk=pk)
    if request.method != "POST":
        messages.error(request, "허용되지 않은 요청입니다.")
        return redirect("reservations:list")

    new_status = request.POST.get("status")
    valid = [s for s, _ in Reservation.STATUS]
    if new_status not in valid:
        messages.error(request, "잘못된 상태 값입니다.")
        return redirect("reservations:list")

    res.status = new_status
    try:
        res.full_clean()
        res.save()  # ✅ DB 반영 → 모든 사용자의 화면은 DB 기준으로 보임
        messages.success(request, "예약 상태가 변경되었습니다.")
    except Exception as e:
        messages.error(request, f"상태 변경 실패: {e}")

    return redirect("reservations:list")
