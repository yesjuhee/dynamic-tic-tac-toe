from django.http import JsonResponse
from django.shortcuts import render
from ..game_logic import check_winner, computer_move
from .base import change_player

# 게임 상태를 저장하는 전역 변수
game_board = [""] * 9
current_player = "X"  # X가 선공
running = True


def practice_mode(request):
    global game_board, current_player, running
    game_board = [""] * 9
    current_player = "X"
    running = True
    status_text = "Your turn"
    return render(
        request,
        "practice_mode.html",
        {"game_board": game_board, "status_text": status_text, "running": running},
    )
