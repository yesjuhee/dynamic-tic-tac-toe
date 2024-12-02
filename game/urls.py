from django.urls import path

from . import views

urlpatterns = [
    # 메인 화면
    path("", views.index, name="index"),
    # 게임 모드
    path("mode/solo/select", views.solo_select, name="solo_select"),  # 1인 모드
    path("mode/solo/<str:user>", views.solo_mode, name="solo_mode"),
    path("mode/couple", views.couple_mode, name="couple_mode"),  # 2인 모드
    path("mode/practice", views.practice_mode, name="practice_mode"),  # 연습 모드
    # 게임 엑션
    path("play/user/<int:cell_index>/", views.user, name="user"),
    path("play/computer/", views.computer, name="computer"),
]
