INFINITY = 1000000
MAX_DEPTH = 10 # Don't know how big I can make this

def get_piece(player, king):
    if player == 1:
        if king == True:
            return 'B'
        else:
            return 'b'
    else:
        if king == True:
            return 'W'
        else:
            return 'w'

def pretty_print_board(board):
    pretty_board = ['-'] * 32
    for piece in board.pieces:
        if piece.position == None:
            continue
        pretty_board[piece.position - 1] = get_piece(piece.player, piece.king)
    print('[ ]' + f'[{pretty_board[0]}]' + '[ ]' + f'[{pretty_board[1]}]' + '[ ]' + f'[{pretty_board[2]}]' + '[ ]' + f'[{pretty_board[3]}]')
    print(f'[{pretty_board[4]}]' + '[ ]' + f'[{pretty_board[5]}]' + '[ ]' + f'[{pretty_board[6]}]' + '[ ]' + f'[{pretty_board[7]}]' + '[ ]')
    print('[ ]' + f'[{pretty_board[8]}]' + '[ ]' + f'[{pretty_board[9]}]' + '[ ]' + f'[{pretty_board[10]}]' + '[ ]' + f'[{pretty_board[11]}]')
    print(f'[{pretty_board[12]}]' + '[ ]' + f'[{pretty_board[13]}]' + '[ ]' + f'[{pretty_board[14]}]' + '[ ]' + f'[{pretty_board[15]}]' + '[ ]')
    print('[ ]' + f'[{pretty_board[16]}]' + '[ ]' + f'[{pretty_board[17]}]' + '[ ]' + f'[{pretty_board[18]}]' + '[ ]' + f'[{pretty_board[19]}]')
    print(f'[{pretty_board[20]}]' + '[ ]' + f'[{pretty_board[21]}]' + '[ ]' + f'[{pretty_board[22]}]' + '[ ]' + f'[{pretty_board[23]}]' + '[ ]')
    print('[ ]' + f'[{pretty_board[24]}]' + '[ ]' + f'[{pretty_board[25]}]' + '[ ]' + f'[{pretty_board[26]}]' + '[ ]' + f'[{pretty_board[27]}]')
    print(f'[{pretty_board[28]}]' + '[ ]' + f'[{pretty_board[29]}]' + '[ ]' + f'[{pretty_board[30]}]' + '[ ]' + f'[{pretty_board[31]}]' + '[ ]')

def print_board_coords():
    print('[  ]' + '[ 1]' + '[  ]' + '[ 2]' + '[  ]' + '[ 3]' + '[  ]' + '[ 4]')
    print('[ 5]' + '[  ]' + '[ 6]' + '[  ]' + '[ 7]' + '[  ]' + '[ 8]' + '[  ]')
    print('[  ]' + '[ 9]' + '[  ]' + '[10]' + '[  ]' + '[11]' + '[  ]' + '[12]')
    print('[13]' + '[  ]' + '[14]' + '[  ]' + '[15]' + '[  ]' + '[16]' + '[  ]')
    print('[  ]' + '[17]' + '[  ]' + '[18]' + '[  ]' + '[19]' + '[  ]' + '[20]')
    print('[21]' + '[  ]' + '[22]' + '[  ]' + '[23]' + '[  ]' + '[24]' + '[  ]')
    print('[  ]' + '[25]' + '[  ]' + '[26]' + '[  ]' + '[27]' + '[  ]' + '[28]')
    print('[29]' + '[  ]' + '[30]' + '[  ]' + '[31]' + '[  ]' + '[32]' + '[  ]')

def get_heuristic_value(board):
    black_pieces = 0
    white_pieces = 0
    for piece in board.pieces:
        if piece.player == 1 and not piece.captured:
            black_pieces += 1
        elif piece.player == 2 and not piece.captured:
            white_pieces += 1
    if board.player_turn == 1:
        return black_pieces / (black_pieces + white_pieces)
    else:
        return white_pieces / (black_pieces + white_pieces)

def alphabeta(state, alpha = -INFINITY, beta = INFINITY, depth = 0):
    # need to deep copy the state, or be able to undo moves
    #print("Board:")
    #pretty_print_board(state.board)
    if state.is_over():
        if state.whose_turn == state.get_winner():
            return 1
        else:
            return -1
    if depth >= MAX_DEPTH:
        return get_heuristic_value(state.board)
    for m in state.get_possible_moves():
        old_board = state.board
        state.move(m)
        value = -alphabeta(state, -beta, -alpha, depth + 1)
        state.board = old_board

        if value > alpha:
            alpha = value
        if value >= beta:
            return beta
    return alpha

def play_move(game):
    moves = game.get_possible_moves()
    ab_results = []
    for i in range(len(moves)):
        print(moves)
        print(ab_results)
        old_board = game.board
        game.move(moves[i])
        ab = alphabeta(game)
        if ab == 1:
            print(f"Found win: {moves[i]}")
            return # This is the best we can do, so keep this move
        ab_results.append(ab)
        game.board = old_board
    print(moves)
    print(ab_results)

    # Pick the move with the best score:
    move_index = ab_results.index(max(ab_results))
    print(f"Playing: {moves[move_index]}")
    game.move(moves[move_index])
