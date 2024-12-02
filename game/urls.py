from django.urls import path

from .views import base, solo, couple, practice

urlpatterns = [
    # 메인 화면
    path("", base.index, name="index"),
    # 1인 모드
    path("mode/solo/select", solo.solo_select, name="solo_select"),
    path("mode/solo/<str:user>", solo.solo_mode, name="solo_mode"),
    path("play/user/solo/<int:cell_index>/", solo.user_solo, name="user_solo"),
    path("play/computer/", solo.computer, name="computer"),
    # 2인 모드
    path("mode/couple", couple.couple_mode, name="couple_mode"),
    path("play/user/couple/<int:cell_index>/", couple.user_couple, name="user_couple"),
    # 연습모드
    path("mode/practice", practice.practice_mode, name="practice_mode"),
    path("play/practice/undo", practice.undo, name="undo"),
    path("play/practice/redo", practice.redo, name="redo"),
    path(
        "play/practice/<int:cell_index>/",
        practice.user_practice,
        name="user_practice",
    ),
]
