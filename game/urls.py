from django.urls import path

from . import views

urlpatterns = [
    # 메인 화면
    path("", views.index, name="index"),
    # 1인 모드
    path(
        "mode/solo/select", views.solo_select, name="solo_select"
    ),  # 1인 모드 선택 화면
    path(
        "mode/solo/<str:user>", views.solo_mode, name="solo_mode"
    ),  # 1인 모드 시작 화면
    path(
        "play/user/solo/<int:cell_index>/", views.user_solo, name="user_solo"
    ),  # 1인 모드 유저 액션
    path("play/computer/", views.computer, name="computer"),  # 1인 모드 컴퓨터 액션
    # 2인 모드
    path("mode/couple", views.couple_mode, name="couple_mode"),  # 2인 모드 시작 화면
    path(
        "play/user/couple/<int:cell_index>/", views.user_couple, name="user_couple"
    ),  # 2인 모드 유저 액션
    path("mode/practice", views.practice_mode, name="practice_mode"),  # 연습 모드
]
