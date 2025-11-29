from django.urls import path
from . import views

app_name = "reservations"
urlpatterns = [
    path("", views.reservation_list, name="list"),
    path("create/", views.reservation_create, name="create"),
    path("<int:pk>/edit/", views.reservation_edit, name="edit"),            # 관리자만
    path("<int:pk>/status/", views.reservation_change_status, name="change_status"),  # ✅ 추가
]
