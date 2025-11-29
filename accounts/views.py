# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .forms import UserUpdateForm


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "회원가입이 완료되었습니다. 로그인해 주세요.")
            return redirect("accounts:login")
    else:
        form = UserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:index")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "로그인되었습니다.")
            # next 파라미터가 있으면 거기로, 없으면 대시보드로
            next_url = request.GET.get("next") or "dashboard:index"
            return redirect(next_url)
    else:
        form = AuthenticationForm(request)
    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_view(request):
    auth_logout(request)
    messages.info(request, "로그아웃되었습니다.")
    return redirect("accounts:login")


@login_required
def profile(request):
    """
    내 계정 정보 보기 (수정 링크 포함)
    """
    return render(request, "accounts/profile.html")


@login_required
def profile_edit(request):
    """
    내 계정 정보 수정 (username, email, first_name, last_name)
    """
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()  # ✅ 여기서 실제 DB에 반영됨
            messages.success(request, "내 계정 정보가 수정되었습니다.")
            return redirect("accounts:profile")
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "accounts/profile_edit.html", {"form": form})
