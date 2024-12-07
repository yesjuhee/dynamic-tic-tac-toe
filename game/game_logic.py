from unittest import result
import random
from numpy import number

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

transformations = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8],  # 기본 보드
    [6, 3, 0, 7, 4, 1, 8, 5, 2],  # 시계방향 90도 회전
    [8, 7, 6, 5, 4, 3, 2, 1, 0],  # 180도
    [2, 5, 8, 1, 4, 7, 0, 3, 6],  # 반시계방향 90도
    [2, 1, 0, 5, 4, 3, 8, 7, 6],  # 좌우 대칭
    [6, 7, 8, 3, 4, 5, 0, 1, 2],  # 상하 대칭
    [0, 3, 6, 1, 4, 7, 2, 5, 8],  # 시계방향 90도 > 좌우 대칭
    [8, 5, 2, 7, 4, 1, 6, 3, 0],  # 반시계방향 90도 > 좌우 대칭
]

# boards = [[""]*9 for _ in range(3**9)] << 모든 보드 구성 만들어놓기?
dp = [[]] * (3**9)

def initialize_dp():
    game_board = [""]*9
    get_dp(game_board, "X")
    return

def board_index(game_board):
    index = 0
    for cell in game_board:
        index *= 3
        if cell == "O":
            index += 2
        elif cell == "X":
            index += 1
    return index
            
def transformation_indices(game_board):
    indices = set()
    for transformation in transformations:
        transformed_board = [game_board[i] for i in transformation]
        indices.add(board_index(transformed_board))
    return indices

def check_winner(game_board, current_turn):
    for condition in win_conditions:
        if (
            game_board[condition[0]] == current_turn
            and game_board[condition[1]] == current_turn
            and game_board[condition[2]] == current_turn
        ):
            return True
    return False

def get_possible_moves(game_board, current_turn, move_sign):
    possible_moves = set()
    for i in range(len(game_board)):
        if game_board[i] == "":
            game_board[i] = current_turn
            if get_dp(game_board, "O" if current_turn == "X" else "X") == move_sign:
                possible_moves.add(i)
            game_board[i] = ""
    return list(possible_moves)

def get_dp(game_board, current_turn):
    index = board_index(game_board)
    
    if dp[index]:
        return dp[index]
    
    opposite_turn = "O" if current_turn == "X" else "X"
    
    if game_board != [""]*9: # 초기상태 예외처리
        if check_winner(game_board, opposite_turn): # 패배
            dp[index] = opposite_turn
            return opposite_turn
    
    if "" not in game_board: # 무승부
        return "T" 
    
    possible_results = set()
    for i in range(len(game_board)):
        if game_board[i] == "":
            game_board[i] = current_turn
            possible_results.add(get_dp(game_board, opposite_turn))
            game_board[i] = ""  
    
    if current_turn in possible_results:
        result = current_turn
    elif "T" in possible_results:
        result = "T"
    else:
        result = opposite_turn
    
    for index in transformation_indices(game_board):
        dp[index] = result
    
    return result
    
start_board = [""]*9
get_dp(start_board, 'X')

def computer_move(game_board, current_turn):
    current_state = get_dp(game_board, current_turn)
    if current_state == current_turn:
        possible_best_moves = get_possible_moves(game_board, current_turn, current_turn)
    elif current_state == "T":
        possible_best_moves = get_possible_moves(game_board, current_turn, "T")
    game_board[random.choice(possible_best_moves)] = current_turn
    return game_board

'''
game_board: 문자열 9개 리스트. 현재 게임 상황 표시
current_turn: 그 다음 차례 ('O' | 'X')
'''
def simulation(game_board, current_turn): 
    simulation_board = game_board
    number = 15
    for i in range(len(simulation_board)):
        if simulation_board[i] == "":
            simulation_board[i] = number
            number += 15
    comment = str(number)
    return simulation_board, comment # gmae_board + ��????��? ��??��?? ��?����??(?????��??) / ��??��??��?? ��??��??��? ??��?? ??��??��??


'''
def minimax(game_board, depth, is_maximizing):
    """
    Minimax algorithm to calculate the optimal move.
    :param game_board: Current state of the game board.
    :param depth: Current depth of the recursion.
    :param is_maximizing: Boolean indicating whether it's the maximizing player's current_turn.
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
