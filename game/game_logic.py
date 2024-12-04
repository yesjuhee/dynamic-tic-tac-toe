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


def computer_move(
    game_board,
    computer_sign,  # TODO : 컴퓨터가 어떤 패인지를 추가함! 상황에 맞춰 수정 필요 ("O"|"X")
):  # TODO : mini-max 혹은 DP가 들어간 로직으로 수정
    for i in range(len(game_board)):
        if game_board[i] == "":
            game_board[i] = computer_sign
            break
    return game_board


"""
game_board: 문자열 9개 리스트. 현재 게임 상황 표시
turn: 그 다음 차례 ('O' | 'X')
"""


def simulation(game_board, turn):
    simulation_board = game_board
    number = 15
    for i in range(len(simulation_board)):
        if simulation_board[i] == "":
            simulation_board[i] = number
            number += 15
    comment = str(number) + "칸이 비어있습니다."
    return (
        simulation_board,
        comment,
    )


'''
def minimax(game_board, depth, is_maximizing):
    """
    Minimax algorithm to calculate the optimal move.
    :param game_board: Current state of the game board.
    :param depth: Current depth of the recursion.
    :param is_maximizing: Boolean indicating whether it's the maximizing player's turn.
    :return: The best score for the current player.
    """
    # Check if the game has reached a terminal state
    if check_winner(game_board, "O"):
        return 10 - depth  # Favor faster wins
    if check_winner(game_board, "X"):
        return depth - 10  # Favor slower losses
    if "" not in game_board:  # Draw
        return 0

    if is_maximizing:
        best_score = float("-inf")
        for i in range(len(game_board)):
            if game_board[i] == "":
                # Try a move
                game_board[i] = "O"
                score = minimax(game_board, depth + 1, False)
                # Undo the move
                game_board[i] = ""
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(len(game_board)):
            if game_board[i] == "":
                # Try a move
                game_board[i] = "X"
                score = minimax(game_board, depth + 1, True)
                # Undo the move
                game_board[i] = ""
                best_score = min(best_score, score)
        return best_score


def computer_move(game_board):
    """
    Use the Minimax algorithm to determine the computer's best move.
    :param game_board: Current state of the game board.
    :return: Updated game board with the computer's move.
    """
    best_score = float("-inf")
    best_move = -1

    for i in range(len(game_board)):
        if game_board[i] == "":
            # Try a move
            game_board[i] = "O"
            score = minimax(game_board, 0, False)
            # Undo the move
            game_board[i] = ""
            if score > best_score:
                best_score = score
                best_move = i

    # Make the best move
    if best_move != -1:
        game_board[best_move] = "O"

    return game_board
'''
