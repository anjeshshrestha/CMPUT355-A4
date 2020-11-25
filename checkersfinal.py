from boardV2 import Board
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
    odd_row = False
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

        if not odd_row: string_to_add += "|.|" 
        elif odd_row and not lone_bar_exists: 
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
        
        if odd_row: string_to_add += "|.|"

        # make new row to print every 4 valid positions
        if index % board.width == 0:
            if not odd_row:
                odd_row = True
                string_to_add += "|"
            else:
                odd_row = False
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

# simulated play between two CPU players
# current_game - the object on which the game is running on
def simulated_play(current_game):
    # assume player 1 is black
    # assume player 2 is white
    game_over = False
    current_player = 0 # for now, first player will be Black
    current_iteration = 1
    last_move = ""
    while game_over == False:
        draw_iteration_details(current_game,current_iteration)

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
    
# checkers game between a person and a CPU
def human_vs_cpu_play(current_game):
    # allow keyboard input
    # make some sort of cli interface
    # determine who goes first

    human_turn = None
    while human_turn == None:
        response = input("Do you want to be first player? (type 'yes'/type anything else for 'no') > ")
        human_turn = True if response == "yes" else False
    
    game_over = None
    #current_player = 1 # Black is 1, White is 2

    iterations = 1
    while not game_over:
        #draw_iteration_details(current_game)
        #draw_board(current_game)
        print("--------------------------------")
        print("Move:",iterations)
        if human_turn: 
            human_play_turn(current_game)
        else:
            cpu_play_turn(current_game)
        
        iterations += 1
        human_turn = not human_turn
        game_over = current_game.get_winner()
    
    print("--------------------------")
    
    print("Final Iteration: " + str(len(current_game.moves) + 1))
    draw_board(current_game)
    print_winner(current_game)

def human_play_turn(current_game):

    permit = False
    current_game.print_board()

    print("Player",current_game.whose_turn(),"- HUMAN PLAY")
    possible_moves = current_game.get_all_valid_moves()
    #print("ugly possible moves:",possible_moves)
    pretty_print_moves(possible_moves)
    response = None
    where_to_move = None
    while True:
        response = int(input("Choose piece to move:" ))
        if response < len(possible_moves):
            break
    piece_to_move = list(possible_moves.keys())[response]

    while True:
        print(possible_moves[piece_to_move])
        where_to_move = int(input("Move to:"))
        if where_to_move < len(list(possible_moves[piece_to_move])):
            break
    current_game.make_moves(possible_moves[piece_to_move][where_to_move])

def pretty_print_moves(dictionary_of_moves):
    piece_index = 0
    for piece_to_move in dictionary_of_moves:
        final = []
        print(piece_index,":",piece_to_move)
        for where in dictionary_of_moves[piece_to_move]:
            final.append(where)
        move_index = 0
        for l in final: 
            print("   ",move_index,">",l)
            move_index += 1
        piece_index += 1
       

# CPU actions for their turn
# current_game  - the object on which the game is running on
# game_strategy - CPUs have the option to employ several playing strategies
# list of game strategies:
# random - CPUs randomly pick valid moves. Considerations of captures not included.
def cpu_play_turn(current_game, game_strategy = 'random'):
    # game_strategies: random, minimax. add and implement if necessary
    if game_strategy == "random":
        current_game.print_board()
        print("Player",current_game.whose_turn(),"- CPU PLAY")

        possible_moves = current_game.get_all_valid_moves()
        pretty_print_moves(possible_moves)

        piece_to_move = None
        where_to_go = None

        random_number = randint(0,len(possible_moves)-1)
        #print("CPU possible moves len",len(possible_moves))
        piece_to_move = list(possible_moves.keys())[random_number]
        length = len(possible_moves[piece_to_move])
        where_to_go = randint(0,length-1)
        
        current_game.make_moves(possible_moves[piece_to_move][where_to_go])
        # random_piece = randint(0,len(possible_moves)-1)
        # current_game.move(possible_moves[move_to_go])
        # print("CPU moved: " + str(possible_moves[move_to_go]))
    else:
        return

# draw the current iteration details
# such as move history, whose turn, and so on.
def draw_iteration_details(current_game):
    print("----------------------------------")
    print()

    current_iteration = len(current_game.moves) + 1
    print("Current Iteration: " + str(current_iteration)) 

    #
    print(current_game.moves)

    current_player = current_game.whose_turn()
    last_move = ''
    print()
    if current_iteration > 1:
        last_move = str(current_game.moves[current_iteration-2])
    print("Player's Turn: Black") if current_game.whose_turn() == 1 else print("Player's Turn: White")
    print("Last move by Previous: " + last_move)

    print()
    print("Overall Move History: " + str(current_game.moves))

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
        #run_away = current_game.move_limit_reached()

        #if run_away:
        #    print(reason_for_loss[0])
        #else:
            print(reason_for_loss[1])
            print("Black wins.") if winner == 1 else print("White wins.")
    else:
        print("No conclusive winner yet.")
    
def main():
    game = Board()
    #draw_board(game)
    game.create_board()
    human_vs_cpu_play(game)

main()