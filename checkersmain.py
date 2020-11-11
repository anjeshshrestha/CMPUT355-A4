from game import Game
import random

# draw_board
# very basic cli function to draw board
# uses the filled positions and the player pieces currently on board
# black is a, white is b
# kings are capitalized (ie. A, B)
# invalid positions are periods or '.'
# (assuming left to right, top to down representation of array)
def draw_board(current_game):
    rows_to_print = []
    string_to_add = ""

    # remember modulo whatever width to know when to cut and add to rows_to_print
    board = current_game.board
    filled_positions = board.searcher.filled_positions
    even_row = False
    # add single bar at beginning of odd row
    lone_bar_exists = False
    printed_index = False

    rows_to_print.append("------------------")

    # iterate through each valid position
    for index in range(1,board.position_count+1):

        current_piece = board.searcher.get_piece_by_position(index)
        if not printed_index: 
            if index < 10:
                string_to_add += "0"
            string_to_add += str(index) + " "
        printed_index = True

        if even_row: string_to_add += "|.|" 
        elif not even_row and not lone_bar_exists: 
            string_to_add += "|"
            lone_bar_exists = True

        # if the current index is occupied, then
        # mark as appropriate
        if index in board.searcher.filled_positions:
            piece_is_king = current_piece.king
            if current_piece in board.searcher.get_pieces_by_player(1):
                if piece_is_king: string_to_add += "A"
                else: string_to_add += "a"
            else:
                if piece_is_king: string_to_add += "B"
                else: string_to_add += "b"
        else:
            string_to_add += "."
        
        if not even_row: string_to_add += "|.|"

        # make new row to print every 4 valid positions
        if index % board.width == 0:
            if even_row:
                even_row = False
                string_to_add += "|"
            else:
                even_row = True
            lone_bar_exists = printed_index = False
            rows_to_print.append(string_to_add)
            string_to_add = ""
    
    for i in rows_to_print:
        print(i)
        



    # for row in range(game.board.height):
    #     for column in range(game.board.width):
    #         current_position = game.board.position_layout[row][column]
    #         print(current_position)
    #         if game.board.position_is_open(current_position):
    #             print("open position")



# letting two people play with legal moves (legal random moves)
# check-list
# set up legal move checker
# set up random
# start game
def simulated_play():
    # plan
    # initialize players
    # start with black
    # then white
    # use random moves just for this
    # make function that determines legality of move

    return


def is_legal(player, board, piece, position):
    # steps to determine if legal
    # basic piece
    # 1) diagonal to your piece?
    # 2) position exists?
    # 2) going to other side of board?
    # 3) is position blank?
    # 4) if enemy on position, is there a blank position in same direction?
    

    # if king, ignore going to other side of board restrictions

    # --------------

    return


    

def black_play(board):
    return

def main():
    game = Game()
    # print(game.board.position_layout)
    # print("--------------------------")
    # print(game.board.position_layout[0][0])

    print()

    #print(game.board.searcher.filled_positions)
    # print(game.board.searcher.player_pieces)
    draw_board(game)
    print(game.get_possible_moves())

    # for row in range(game.board.height):
    #     for column in range(game.board.width):
    #         current_position = game.board.position_layout[row][column]
    #         print(current_position)
    #         if game.board.position_is_open(current_position):
    #             print("open position")
    #         # print(game.board.searcher.get_piece_by_position(current_position))
    #         # print()

main()