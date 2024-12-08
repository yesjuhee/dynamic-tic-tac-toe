from django.http import JsonResponse
from django.shortcuts import render
from ..game_logic import check_winner, simulation
from .base import change_player

# 게임 상태를 저장하는 전역 변수
game_board = [""] * 9
current_player = "X"  # X가 선공
running = True

# 상태 기록 스택
history = []
future = []


def practice_mode(request):
    global game_board, current_player, running
    game_board = [""] * 9
    current_player = "X"
    running = True
    history = []
    future = []
    status_text = "X 의 차례입니다."
    analyses = "여기에 분석 결과가 표시됩니다."
    return render(
        request,
        "practice_mode.html",
        {
            "game_board": game_board,
            "status_text": status_text,
            "running": running,
            "analyses": analyses,
        },
    )


def user_practice(request, cell_index):
    global game_board, current_player, running, history, future

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
                "analyses": "다시 선택해주세요.",
            }
        )

    history.append((game_board.copy(), current_player, running))
    future.clear()

    # 유저의 위치 표시
    game_board[cell_index] = current_player

    # 유저 승리 여부 확인
    if check_winner(game_board, current_player):
        running = False
        return JsonResponse(
            {
                "game_board": game_board,
                "status_text": current_player + " 가 승리하였습니다.",
                "running": running,
                "analyses": "게임 종료",
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
                "analyses": "게임 종료",
            }
        )

    current_player = change_player(current_player)
    
    simulation_board, analyses = simulation(game_board.copy(), current_player, initial_depth=game_board.count(""))

    return JsonResponse(
        {
            "game_board": simulation_board,
            "status_text": current_player + " 의 차례입니다.",
            "running": running,
            "comment": analyses,
        }
    )


def undo(request):
    global game_board, current_player, running, history, future

    if not history:
        return JsonResponse(
            {
                "game_board": game_board,
                "status_text": current_player + " 의 차례입니다.",
                "running": running,
                "comment": "이전 상태가 없습니다.",
            }
        )

    future.append((game_board.copy(), current_player, running))
    game_board, current_player, running = history.pop()

    # 맨 처음 상황일 경우 예외처리
    if ("X" not in game_board) and ("O" not in game_board):
        return JsonResponse(
            {
                "game_board": game_board,
                "status_text": current_player + " 의 차례입니다.",
                "running": running,
                "comment": "여기에 분석 결과가 표시됩니다.",
            }
        )

    simulation_board, comment = simulation(game_board.copy(), current_player)

    return JsonResponse(
        {
            "game_board": simulation_board,
            "status_text": current_player + " 의 차례입니다.",
            "running": running,
            "comment": comment,
        }
    )


def redo(request):
    global game_board, current_player, running, history, future

    if not history:
        return JsonResponse(
            {
                "game_board": game_board,
                "status_text": current_player + " 의 차례입니다.",
                "running": running,
                "comment": "다음 상태가 없습니다.",
            }
        )

    history.append((game_board.copy(), current_player, running))
    game_board, current_player, running = future.pop()
    simulation_board, comment = simulation(game_board.copy(), current_player)

    return JsonResponse(
        {
            "game_board": simulation_board,
            "status_text": current_player + " 의 차례입니다.",
            "running": running,
            "comment": comment,
        }
    )
