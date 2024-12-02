from django.http import JsonResponse
from django.shortcuts import render
from ..game_logic import check_winner, computer_move
from .base import change_player

# 게임 상태를 저장하는 전역 변수
game_board = [""] * 9
current_player = "X"  # X가 선공
running = True


def couple_mode(request):
    global game_board, current_player, running
    game_board = [""] * 9
    current_player = "X"
    running = True
    status_text = "X 의 차례입니다."
    return render(
        request,
        "couple_mode.html",
        {"game_board": game_board, "status_text": status_text, "running": running},
    )


def user_couple(request, cell_index):
    global game_board, current_player, running

    if not running:
        return JsonResponse(
            {"game_board": game_board, "status_text": "게임 종료", "running": running}
        )

    cell_index = int(cell_index)

    if game_board[cell_index] != "":
        return JsonResponse(
            {
                "game_board": game_board,
                "status_text": "잘못된 위치입니다!",
                "running": running,
            }
        )

    # 유저의 위치 표시
    game_board[cell_index] = current_player

    # 유저 승리 여부 확인
    if check_winner(game_board, current_player):
        running = False
        return JsonResponse(
            {
                "game_board": game_board,
                "status_text": current_player + " 의 승리를 축하합니다!",
                "running": running,
            }
        )

    # 보드가 꽉 찬 경우 확인
    if "" not in game_board:
        running = False
        return JsonResponse(
            {
                "game_board": game_board,
                "status_text": "비겼습니다!",
                "running": running,
            }
        )

    change_player()

    return JsonResponse(
        {
            "game_board": game_board,
            "status_text": current_player + " 의 차례입니다.",
            "running": running,
        }
    )
