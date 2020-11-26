from board import Board
from alphabeta import play_move

def main():
    board = Board()

    while not board.has_winner():
        # First get user input for white
        board.print_board()
        valid_moves = board.print_all_valid_moves()
        print(valid_moves)
        print("Select a piece to move:")
        piece_row = int(input("row: "))
        piece_col = int(input("column: "))
        if (piece_row, piece_col) not in valid_moves:
            print("Not a valid piece")
            continue
        print("Select move to make (by index): ")
        moves_for_piece = valid_moves[piece_row, piece_col]
        print(moves_for_piece)
        move_index = int(input())
        if move_index > len(moves_for_piece):
            print("Not a valid move index")
            continue
        move = moves_for_piece[move_index][1]
        board.make_moves([(piece_row, piece_col), (move[0], move[1])])
        board.print_board()

        # Now let our player play for black
        play_move(board)

main()