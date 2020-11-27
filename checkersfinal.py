from board import Board
from random import randint
from sys import flags, exit
from pygame_board import pygame,PyGameBoard
import alphabeta

ALPHABETA = 'alphabeta'
RANDOM = 'random'

def human_vs_alphabeta_no_gui(board):
    # Use this function to play without the pygame gui
    # Loop while we don't have a winner
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
        print("Thinking....")
        alphabeta.play_move(board)

def random_vs_alphabeta_no_gui():
    # Pit a random player against an alphabeta player
    # Random is player 1, alphabeta is player 2
    board = Board()
    print(f"Random player: {board.player}")
    while not board.has_winner():
        board.print_board()
        # Random player plays
        possible_moves = board.get_all_valid_moves()
        random_number = randint(0, len(possible_moves) - 1)
        piece_to_move = list(possible_moves.keys())[random_number]
        length = len(possible_moves[piece_to_move])
        where_to_go = randint(0, length - 1)
        board.make_moves(possible_moves[piece_to_move][where_to_go])

        if board.has_winner():
            break

        # Alphabeta player plays
        board.print_board()
        alphabeta.play_move(board)
    return board.get_winner_code()

def alphabeta_vs_random_no_gui():
    # Pit a random player against an alphabeta player
    # Alphabeta is player 1, random is player 2
    board = Board()
    print(f"Random player: {board.player}")
    while not board.has_winner():
        board.print_board()
        # Random player plays
        possible_moves = board.get_all_valid_moves()
        random_number = randint(0, len(possible_moves) - 1)
        piece_to_move = list(possible_moves.keys())[random_number]
        length = len(possible_moves[piece_to_move])
        where_to_go = randint(0, length - 1)
        board.make_moves(possible_moves[piece_to_move][where_to_go])

        if board.has_winner():
            break

        # Alphabeta player plays
        board.print_board()
        alphabeta.play_move(board)
    return board.get_winner_code()

def get_stats():
    # Play the alphabeta player vs the random player and get stats on who wins
    iterations = 10
    results = []
    for i in range(iterations):
        results.append(random_vs_alphabeta_no_gui())
    for i in range(iterations):
        results.append(alphabeta_vs_random_no_gui())
    print(results)
    return results

# checkers game between a person and a random player
def human_vs_random_play(current_game, pygame_instance = None, play_strategy = ALPHABETA):
    # allow keyboard input
    # make some sort of cli interface
    # determine who goes first

    clock = pygame.time.Clock()
    framerate = 2

    human_turn = False
    simulate_play = False
    
    response = input("Do you want to be first player? \n(To simulate, type 'simulate') (type 'yes', type anything else to be second.) > ")

    play_type = int(input("Will computer make (1)random or (2)AlphaBeta move: "))
    if play_type == 1:
        play_strategy = RANDOM
    else:
        play_strategy = ALPHABETA

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
        print("Move: ",iterations)
        print("Player",current_game.whose_turn(),"- HUMAN PLAY") if human_turn else print("Player",current_game.whose_turn(),"- CPU PLAY")

        current_game.print_board()

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

def play_turn(current_game, is_human = False, game_strategy = ALPHABETA):
    possible_moves = current_game.get_all_valid_moves()
    pretty_print_moves(possible_moves)
    piece_to_move = None
    where_to_go = None

    if is_human:
        response = None
        while True:
            print("To quit, simply type a negative number.")
            response = int(input("Choose piece to move (by index): " ))
            if response < len(possible_moves):
                break
            
        if response < 0:
            #pygame.quit()
            exit()
        
        piece_to_move = list(possible_moves.keys())[response]

        while True:
            #print(possible_moves[piece_to_move])
            where_to_go = int(input("Move to (by index): "))
            if where_to_go < len(list(possible_moves[piece_to_move])):
                current_game.make_moves(possible_moves[piece_to_move][where_to_go])
                break
    else:
        if game_strategy == RANDOM:
            random_number = randint(0,len(possible_moves)-1)
            print("Random player possible moves len",len(possible_moves))
            piece_to_move = list(possible_moves.keys())[random_number]
            length = len(possible_moves[piece_to_move])
            where_to_go = randint(0,length-1)
            
            # random_piece = randint(0,len(possible_moves)-1)
            # current_game.move(possible_moves[move_to_go])
            # print("CPU moved: " + str(possible_moves[move_to_go]))
            current_game.make_moves(possible_moves[piece_to_move][where_to_go])
        elif game_strategy == ALPHABETA:
            print("Thinking....")
            alphabeta.play_move(current_game)

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
    board = Board()
    pygame_board = PyGameBoard()

    human_vs_random_play(board, pygame_board)
    #human_vs_alphabeta(board)

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
    pygame_board.create_board(board.board)
    pygame.display.update()

    #game.print_board()
    #human_vs_cpu_play(game)

def test_bench():
    game = Board()
    game.create_board()

if __name__ == "__main__" and not flags.interactive:
    main()
    input()
