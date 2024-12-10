import random
from turtle import position
import numpy as np
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

start_board = [""]*9
# boards = [[""]*9 for _ in range(3**9)] << 모든 보드 구성 만들어놓기?
dp_state = [""] * (3**9)
dp_prob = [[""]*9] * (3**9)

def initialize_dp():
    game_board = [""]*9
    get_dp(game_board, "X")
    simulation(game_board, "X", 9)
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
    for i, cell in enumerate(game_board):
        if cell == "":
            game_board[i] = current_turn
            if get_dp(game_board, "O" if current_turn == "X" else "X") == move_sign:
                possible_moves.add(i)
            game_board[i] = ""
    return list(possible_moves)

def get_instant_wins(game_board, current_turn):
    win_moves = set()
    for i, cell in enumerate(game_board):
        if cell == "":
            game_board[i] = current_turn
            if check_winner(game_board, current_turn):
                win_moves.add(i)
            game_board[i] = ""
    return list(win_moves)

def get_dp(game_board, current_turn):
    index = board_index(game_board)
    
    if dp_state[index]:
        return dp_state[index]
    
    opposite_turn = "O" if current_turn == "X" else "X"
    
    if game_board != start_board: # 초기상태 예외처리
        if check_winner(game_board, opposite_turn): # 패배
            dp_state[index] = opposite_turn
            return opposite_turn
    
    if "" not in game_board: # 무승부
        return "T" 
    
    possible_results = set()
    for i, cell in enumerate(game_board):
        if cell == "":
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
        dp_state[index] = result
    
    return result
    
get_dp(start_board, 'X')

def computer_move(game_board, current_turn):
    if game_board == start_board:
        game_board[random.randrange(0,9)] = current_turn
        return game_board
    current_state = get_dp(game_board, current_turn)
    win_moves = get_instant_wins
    if win_moves:
        possible_best_moves = win_moves
    elif current_state == current_turn:
        possible_best_moves = get_possible_moves(game_board, current_turn, current_turn)
    elif current_state == "T":
        possible_best_moves = get_possible_moves(game_board, current_turn, "T")
    game_board[random.choice(possible_best_moves)] = current_turn
    return game_board

'''
game_board: 문자열 9개 리스트. 현재 게임 상황 표시
current_turn: 그 다음 차례 ('O' | 'X')
'''
def simulation(game_board, current_turn, move_weights=(20, 10, 1)): 
    comment = "comment"
    
    initial_index = board_index(game_board)
    if "" not in dp_prob[initial_index]:
        return dp_prob[initial_index], comment
    
    simulation_board = game_board.copy()
    opposite_turn = "O" if current_turn == "X" else "X"
    
    def simulate(prev_game_board, prev_board_index, turn, cell_index):
        if "" not in dp_prob[prev_board_index] and type(dp_prob[prev_board_index][cell_index]) == float:
            return dp_prob[prev_board_index][cell_index]
        
        prev_game_board[cell_index] = turn
        if check_winner(prev_game_board, turn):
            return 1
        if "" not in prev_game_board:
            return 0.5
        
        cur_game_board = prev_game_board.copy()
        prev_game_board[cell_index] = ""
        cur_board_index = board_index(cur_game_board)
        dp_prob[cur_board_index] = cur_game_board.copy()
        
        next_turn = "O" if turn == "X" else "X"
        values = []
        for i, cell in enumerate(cur_game_board):
            if cell == "":
                expected_value = simulate(cur_game_board, cur_board_index, next_turn, i)
                values.append(expected_value)
                dp_prob[cur_board_index][i] = expected_value
        
        for transform in transformations:
            transformed_index = board_index([cur_game_board[i] for i in transform])
            dp_prob[transformed_index] = [dp_prob[cur_board_index][i] for i in transform]
        
        weights = [
            move_weights[0] if value == 1
            else move_weights[1] if value == 0.5
            else move_weights[2] for value in values
        ]
        
        weights_sum = sum(weights)
        return round(1 - sum(value * weight / weights_sum for value, weight in zip(values, weights)), 2)
    
    for i in range(len(game_board)):
        if game_board[i] == "":
            simulation_board[i] = simulate(game_board, initial_index, current_turn, i)
    
    for transform in transformations:
        transformed_index = board_index([game_board[i] for i in transform])
        dp_prob[transformed_index] = [simulation_board[i] for i in transform]
        
    return simulation_board, comment # game_board + ��????��? ��??��?? ��?����??(?????��??) / ��??��??��?? ��??��??��? ??��?? ??��??��??

    # board_size = len(game_board)
    #  # 승/무/패 가중치
    # for i in range(board_size):
    #     move_value = 0
    #     if game_board[i] == "":
    #         game_board[i] = current_turn
    #         first_value_board = np.zeros((board_size, 2)).tolist()
    #         first_z`weight_sum = 0
    #         for j in range(board_size): # 상대의 대응수
    #             if game_board[j] == "":
    #                 game_board[j] = opposite_turn
    #                 if get_dp(game_board, current_turn) == current_turn:
    #                     first_value_board[j][0] = move_weights[0]
    #                 elif get_dp(game_board, current_turn) == opposite_turn:
    #                     first_value_board[j][0] = move_weights[2]
    #                 else:
    #                     first_value_board[j][0] = move_weights[1]
    #                 first_weight_sum += first_value_board[j][0]
                    
    #                 second_value_board = np.zeros((board_size, 2)).tolist()
    #                 second_weight_sum = 0
    #                 for k in range(board_size): # 대응수에 대한 그 다음 수
    #                     if game_board[k] == "":
    #                         game_board[k] = current_turn
    #                         if get_dp(game_board, opposite_turn) == opposite_turn:
    #                             second_value_board[k][0] = move_weights[0]
    #                         elif get_dp(game_board, opposite_turn) == current_turn:
    #                             second_value_board[k][0] = move_weights[2]
    #                         else:
    #                             second_value_board[k][0] = move_weights[1]
    #                         second_weight_sum += second_value_board[k][0]
                            
    #                         third_value_board = np.zeros((board_size, 2)).tolist()
    #                         third_weight_sum = 0
    #                         for l in range(board_size):
    #                             if game_board[l] == "":
    #                                 game_board[l] = opposite_turn
    #                                 if get_dp(game_board, current_turn) == current_turn:
    #                                     third_value_board[l] = [move_weights[0], 1]
    #                                 elif get_dp(game_board, current_turn) == opposite_turn:
    #                                     third_value_board[l] = [move_weights[2], 0]
    #                                 else:
    #                                     third_value_board[l] = [move_weights[1], 0.5]
    #                                 third_weight_sum += third_value_board[l][0]
    #                                 game_board[l] = ""
    #                         if third_weight_sum:
    #                             for l in range(board_size):
    #                                 second_value_board[l][1] += (third_value_board[l][0] / third_weight_sum) * third_value_board[l][1]
    #                         else:
    #                             for l in range(board_size):
    #                                 if second_value_board[l][1] == move_weights[0]:
    #                                     second_value_board[l][1] = 1
    #                                 elif second_value_board[l][1] == move_weights[1]:
    #                                     second_value_board[l][1] = 0.5
    #                                 else:
    #                                     second_value_board[l][1] = 0
    #                         game_board[k] = ""
    #                 if second_weight_sum:
    #                     for k in range(board_size):
    #                         first_value_board[j][1] += (second_value_board[k][0] / second_weight_sum) * second_value_board[k][1]
    #                 else:
    #                     for k in range(board_size):
    #                         if first_value_board[k][1] == move_weights[0]:
    #                             first_value_board[k][1] = 1
    #                         elif first_value_board[k][1] == move_weights[1]:
    #                             first_value_board[k][1] = 0.5
    #                         else:
    #                             first_value_board[k][1] = 0
    #                 game_board[j] = ""
    #         if first_weight_sum:
    #             for j in range(board_size):
    #                 move_value += (first_value_board[j][0] / first_weight_sum) * first_value_board[j][1]
    #         game_board[i] = ""
            
    #         simulation_board[i] = round(move_value, 2)

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
