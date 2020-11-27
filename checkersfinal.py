from board import Board
from random import randint
from time import sleep
from sys import exit
from pygame_board import pygame,PyGameBoard

####
# For quick settings changes

SLEEP_DURATION = 1         # PyGame board switches too fast, this keeps it under control
                           # Make 0 to speed up simulations, sleep function uses seconds.
DEBUG_MODE     = False     # Turn on printing of variables.
CPU_STRATEGY   = 'random'  # Currently available are: 'random',...
PYGAME_BOARD   = True      # Use the PyGameBoard. PyGame must be installed on your system.

####

# checkers game between a person and a CPU
# simulation between two CPUs can occur.
# -
# additional features: differing CPU strategies, ...
# -
# current_game    - the Board object that handles the game
# pygame_instance - the PyGameClass object that draws the PyGame board.
def human_vs_cpu_play(current_game,pygame_instance = None):
    human_turn = simulate_play = False
    
    response = input("Do you want to be first player? \n(type 'yes', type anything else to be second.)\n(To simulate, type 'simulate') > ")
     
    if response == "yes":
        human_turn = True
    elif response == 'simulate':
        simulate_play = True

    game_over = False

    number_of_moves = 1
    while not game_over:
        print("--------------------------------")
        print("Move:",number_of_moves)
        print("Player",current_game.whose_turn(),"- HUMAN PLAY") if human_turn else print("Player",current_game.whose_turn(),"- CPU PLAY")
        print("Color: WHITE") if current_game.whose_turn() == 1 else print("Color: RED")

        print("Move History:",current_game.moves)

        print()

        current_game.print_board()

        if DEBUG_MODE:
            print("player 1 pieces count",current_game.player1PiecesCount)
            print("player 2 pieces count",current_game.player2PiecesCount)
        
        if pygame_instance:
            # for some reason, PyGame has issues if these events aren't handled with.
            # that's why it's passed.
            # Since PyGame is used for visual only, CLI is still primary way to play the game.
            for event in pygame.event.get(): pass

            pygame_instance.create_board(current_game.board) # this updates the board copy in the game class
            pygame.display.update()
            play_turn(current_game,human_turn,CPU_STRATEGY) 
            sleep(SLEEP_DURATION) # Normally, modern computers blaze through simulations
                                  # This throttles so we can see it happen at a reasonable pace.
        else:
            play_turn(current_game,human_turn,CPU_STRATEGY)
        
        number_of_moves += 1

        if not simulate_play: human_turn = not human_turn

        game_over = current_game.has_winner()
    
    print("--------------------------------")
    
    print("Final Move:",number_of_moves)
    current_game.print_board()
    current_game.get_winner()
    exit()


# play a turn on the checkers board
# can handle both human and CPU algorithms
# -
# current_game  - the Board object that handles the game
# is_human      - determine whether to allow human input or use a CPU strategy
# game_strategy - the game strategy for the CPU. By default, it is random.
def play_turn(current_game,is_human = False,game_strategy = 'random'):
    possible_moves = current_game.get_all_valid_moves()

    if is_human: pretty_print_moves(possible_moves)
    if not is_human and DEBUG_MODE: pretty_print_moves(possible_moves)

    piece_to_move = where_to_go = None

    if is_human:
        response = None
        while True:
            print("To quit, simply type a negative number.")
            response = int(input("Choose piece to move:" ))
            if response < len(possible_moves):
                break
            
        if response < 0:
            #input()
            #pygame.quit() 
            exit()
        
        piece_to_move = list(possible_moves.keys())[response]

        while True:
            print(possible_moves[piece_to_move])
            where_to_go = int(input("Move to:"))
            if where_to_go < len(list(possible_moves[piece_to_move])):
                break
    else:
        if game_strategy == "random":
            random_number = randint(0,len(possible_moves)-1)
            if DEBUG_MODE: print("CPU possible moves len",len(possible_moves))
            piece_to_move = list(possible_moves.keys())[random_number]
            length = len(possible_moves[piece_to_move])
            where_to_go = randint(0,length-1)
        
    current_game.make_moves(possible_moves[piece_to_move][where_to_go])

# print the list of possible moves
# -
# dictionary_of_moves - a dictionary containing pieces as keys and possible positions as elements
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


def main():
    game = Board()
    game.create_board()
    pygame_board = PyGameBoard() if PYGAME_BOARD else None
    human_vs_cpu_play(game,pygame_board)

main()
input()

