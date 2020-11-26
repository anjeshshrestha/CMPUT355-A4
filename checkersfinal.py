from board import Board
from random import randint
from time import sleep
import sys
from pygame_board import pygame,PyGameBoard

# DEPRECIATED
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

# NOT CONVERTED FOR V2 BOARD
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
def human_vs_cpu_play(current_game,pygame_instance = None):
    # allow keyboard input
    # make some sort of cli interface
    # determine who goes first

    clock = pygame.time.Clock()
    framerate = 2

    human_turn = False
    simulate_play = False
    
    #response = input("Do you want to be first player? \n(To simulate, type 'simulate') (type 'yes', type anything else to be second.) > ")
    response = "simulate"
    if response == "yes":
        human_turn = True
    elif response == 'simulate':
        simulate_play = True

    
    game_over = False
    #current_player = 1 # Black is 1, White is 2

    iterations = 1
    while not game_over:
        #draw_iteration_details(current_game)
        #draw_board(current_game)
        print("--------------------------------")
        print("Move:",iterations)
        print("Player",current_game.whose_turn(),"- HUMAN PLAY") if human_turn else print("Player",current_game.whose_turn(),"- CPU PLAY")

        current_game.print_board()
        play_strategy = 'random'

        print("player 1 pieces count",current_game.player1PiecesCount)
        print("player 2 pieces count",current_game.player2PiecesCount)

        if pygame_instance:
            for event in pygame.event.get():pass
            pygame_instance.create_board(current_game.board)
            pygame.display.update()
            play_turn(current_game,human_turn,play_strategy)
            #sleep(1)
            
        else:
            play_turn(current_game,human_turn,play_strategy)
        iterations += 1
        if not simulate_play:
            human_turn = not human_turn

        game_over = current_game.has_winner()
    
    print("--------------------------")
    
    print("Final Iteration: " + str(len(current_game.moves) + 1))
    current_game.print_board()
    print(current_game.get_winner())
    #print_winner(current_game)


def play_turn(current_game,is_human = False,game_strategy = 'random'):
    possible_moves = current_game.get_all_valid_moves()
    if is_human: pretty_print_moves(possible_moves)
    if not is_human: pretty_print_moves(possible_moves)
    piece_to_move = None
    where_to_go = None

    if is_human:
        response = None
        while True:
            print("To quit, simply type a negative number.")
            response = int(input("Choose piece to move:" ))
            if response < len(possible_moves):
                break
            
        if response < 0:
            pygame.quit() 
            sys.exit()
        
        piece_to_move = list(possible_moves.keys())[response]

        while True:
            #print(possible_moves[piece_to_move])
            where_to_go = int(input("Move to:"))
            if where_to_go < len(list(possible_moves[piece_to_move])):
                break
    else:
        if game_strategy == "random":
            random_number = randint(0,len(possible_moves)-1)
            print("CPU possible moves len",len(possible_moves))
            piece_to_move = list(possible_moves.keys())[random_number]
            length = len(possible_moves[piece_to_move])
            where_to_go = randint(0,length-1)
            
            # random_piece = randint(0,len(possible_moves)-1)
            # current_game.move(possible_moves[move_to_go])
            # print("CPU moved: " + str(possible_moves[move_to_go]))
    current_game.make_moves(possible_moves[piece_to_move][where_to_go])

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
    # game_strategies: random, ... add and implement if necessary
    if game_strategy == "random":
        current_game.print_board()
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

# DEPRECIATED
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
    pygame_board = PyGameBoard()

    human_vs_cpu_play(game,pygame_board)

    #run_window(game,pygame_board)
    

#def run_window(current_game,visual_board):
   
    # running = True
    # while running:
    #     clock.tick(framerate)
    #     for event in pygame.event.get():
    #         print("pygame event",pygame.event.get())
    #         # if event.type == pygame.QUIT:
    #         #     pygame.quit()
    #         #     sys.quit()
    #         #     running = False
    #ygame.display.set_caption("Checkers")

    pygame.display.update()

    #game.print_board()
    #human_vs_cpu_play(game)

def test_bench():
    game = Board()
    game.create_board()


main()
