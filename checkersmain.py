from game import Game
from random import randint
from time import sleep

# draw_board
# very basic cli function to draw board
# uses the filled positions and the player pieces currently on board
# black is b, white is w
# kings are capitalized (ie. B, W)
# invalid positions are periods or '.'
# valid positions, not including player legality, are "#"
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

    rows_to_print.append("- Black Origin - ")

    rows_to_print.append("--------------------")

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
                if piece_is_king: string_to_add += "B"
                else: string_to_add += "b"
            else:
                if piece_is_king: string_to_add += "W"
                else: string_to_add += "w"
        else:
            string_to_add += "#"
        
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
            rows_to_print.append("--------------------")
            string_to_add = ""
    
    rows_to_print.append("- White Origin -")
    for i in rows_to_print:
        print(i)
        
    # for row in range(game.board.height):
    #     for column in range(game.board.width):
    #         current_position = game.board.position_layout[row][column]
    #         print(current_position)
    #         if game.board.position_is_open(current_position):
    #             print("open position")

# letting two people play with legal moves (legal random moves)
def simulated_play(current_game):
    # assume player 1 is black
    # assume player 2 is white
    game_over = False
    current_player = 0 # for now, first player will be Black
    current_iteration = 1
    last_move = ""
    while game_over == False:
        print("----------------------------------")
        print()

        print("Current Iteration: " + str(current_iteration))
        current_iteration += 1

        current_player = current_game.whose_turn()

        print("Player's Turn: Black") if current_player == 1 else print("Player's Turn: White")
        print("Last move by Previous: " + last_move)

        print()
        print("Overall Move History: " + str(current_game.moves))

        draw_board(current_game)

        possible_moves = current_game.get_possible_moves()
        random_number = randint(0, len(possible_moves)-1)

        last_move = str(possible_moves[random_number])

        current_game.move(possible_moves[random_number])

        print()

        game_over =  current_game.is_over()
    
    
    print("--------------------------")
    
    print("Final Iteration: " + str(current_iteration))
    draw_board(current_game)

    print_winner(current_game)
    


# print_winner(current_game)
# current_game - an active Game object that handles the checker game.
#
# when game is over,
# print the winner and why they won.
# a circumstance exists where both players continuously run away from each other
# thus, no winner can be deduced. This is automatically determined after
# 40 consecutive moves without a capture.
# if no winner, print "No conclusive winner yet."
# By default, Black is player 1, White is player 2.

def print_winner(current_game):
    if current_game.is_over():
        winner = current_game.get_winner()
        reason_for_loss = ["The previous player has moved 40 times without a capture. There is no winner." , 
                           "The winner captured the last opponent piece, thus ending the game."]
        run_away = current_game.move_limit_reached()

        if run_away:
            print(reason_for_loss[0])
        else:
            print(reason_for_loss[1])
            print("Black wins.") if winner == 1 else print("White wins.")
    else:
        print("No conclusive winner yet.")
    
def main():
    game = Game()
    #draw_board(game)
    simulated_play(game)

main()