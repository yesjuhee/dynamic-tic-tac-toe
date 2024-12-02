from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .game_logic import check_winner, computer_move


# 게임 상태를 저장하는 전역 변수
game_board = [""] * 9
current_player = "X"  # X가 선공
running = True
win_conditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]


def index(request):
    return render(request, "index.html")


def solo_select(request):
    return render(request, "solo_select.html")


def solo_mode(request, user):
    global game_board, current_player, running
    game_board = [""] * 9  # 게임 보드 초기화
    running = True
    current_player = "X"

    if user == "O":  # 컴퓨터가 선인경우
        computer(request)
    
    status_text = "유저의 차례입니다."

    return render(
        request,
        "solo_mode.html",
        {"game_board": game_board, "status_text": status_text, "running": running},
    )


def couple_mode(request):
    global game_board, current_player, running
    game_board = [""] * 9
    current_player = "X"
    running = True
    status_text = "X's turn"
    return render(
        request,
        "couple_mode.html",
        {"game_board": game_board, "status_text": status_text, "running": running},
    )


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


def user(request, cell_index):
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
            {"game_board": game_board, "status_text": "승리를 축하합니다!", "running": running}
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
    
    change_player() # 컴퓨터 차례
    
    return JsonResponse(
        {"game_board": game_board, "status_text": "컴퓨터 차례입니다.", "running": running}
    )


def computer(request):
    global game_board, current_player, running

    if not running:
        return JsonResponse(
            {"game_board": game_board, "status_text": "게임 종료", "running": running}
        )

    # 컴퓨터 위치 결정
    game_board = computer_move(game_board, current_player)

    # 컴퓨터 승리 여부 확인
    if check_winner(game_board, current_player):
        running = False
        return JsonResponse(
            {"game_board": game_board, "status_text": "패배했습니다...", "running": running}
        )

    # 보드가 꽉 찬 경우 확인
    if "" not in game_board:
        running = False
        return JsonResponse(
            {
                "game_board": game_board,
                "status_text": "It's a draw!",
                "running": running,
            }
        )

    # 유저 차레로 바뀜
    change_player()
    return JsonResponse(
        {"game_board": game_board, "status_text": "유저의 차례입니다.", "running": running}
    )


def change_player():
    global current_player
    if current_player == "X":
        current_player = "O"
    else:
        current_player = "X"
