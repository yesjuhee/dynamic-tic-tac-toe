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


def check_winner(game_board, current_player):
    for condition in win_conditions:
        if (
            game_board[condition[0]] == current_player
            and game_board[condition[1]] == current_player
            and game_board[condition[2]] == current_player
        ):
            return True
    return False


def computer_move(game_board):
    for i in range(len(game_board)):
        if game_board[i] == "":
            game_board[i] = "O"  # Computer always plays as "O"
            break
    return game_board
