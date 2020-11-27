from copy import deepcopy
import random

INFINITY = 1000000
MAX_DEPTH = 4 # The bigger the better
WIN = 100
LOSS = -100

def alphabeta(board, alpha = -INFINITY, beta = INFINITY, depth = 0):
    if board.has_winner():
        if board.to_play_won():
            return WIN
        else:
            return LOSS
    if depth >= MAX_DEPTH:
        heuristic = board.get_board_heuristic()
        return heuristic
    moves = board.get_all_valid_moves_as_list()
    for move in moves:
        board_copy = deepcopy(board)
        if isinstance(move[0], list):
            print(move)
            test = board.get_all_valid_moves()
            print(test)
        board_copy.make_moves(move)
        value = -alphabeta(board_copy, -beta, -alpha, depth + 1)
        if value > alpha:
            alpha = value
        if value >= beta:
            return beta
    return alpha

def play_move(board):
    moves = board.get_all_valid_moves_as_list()
    ab_results = []
    if len(moves) == 1:
        print(f'Only one move: {moves[0]}')
        board.make_moves(moves[0])
        return
    for i in range(len(moves)):
        #print(moves)
        #print(ab_results)
        board_copy = deepcopy(board)
        board_copy.make_moves(moves[i])
        ab = -alphabeta(board_copy)
        if ab == WIN:
            print(f'Found win: {moves[i]}')
            board.make_moves(moves[i])
            return # This is the best we can do, so keep this move
        ab_results.append(ab)
    #print(moves)
    #print(ab_results)

    # Pick the move with the best score
    # If multiple moves with a best score, pick one at random
    if len(ab_results) == 0:
        return # Got called when we shouldn't have, don't make a move
    max_score = max(ab_results)
    move_index = random.choice([i for i in range(len(ab_results)) if ab_results[i] == max_score])
    move = moves[move_index]
    print(f'Playing: {move}')
    board.make_moves(move)

