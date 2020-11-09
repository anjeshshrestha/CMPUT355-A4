INFINITY = 1000000
MAX_DEPTH = 50 # Don't know how big I can make this

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

def alphabeta(state, alpha = -INFINITY, beta = INFINITY, depth = 0):
    # need to deep copy the state, or be able to undo moves
    print("Board:")
    pretty_print_board(state.board)
    old_board = state.board
    if state.is_over():
        if state.whose_turn == state.get_winner():
            return 1
        else:
            return -1
    if depth >= MAX_DEPTH:
        return 0 # return draw
    for m in state.get_possible_moves():
        state.move(m)
        value = -alphabeta(state, -beta, -alpha, depth + 1)
        if value > alpha:
            alpha = value
        state.board = old_board
        if value >= beta:
            return beta
    return alpha