import pygame
from piece import Piece

#board dimensions
(WIDTH, HEIGHT) = (600,600)
BROWN = (156, 117, 0)
BLACK = (0, 0, 0)
WHITE = (255,255,255)
GREY  = (177,177,177)
RED   = (255,0,0)
PINK  = (255, 128, 128)

class PyGameBoard:
    def __init__(self, width = WIDTH, height = HEIGHT, rows = 8, cols = 8):
        pygame.init()
        self.width = WIDTH
        self.height = HEIGHT
        self.rows = rows
        self.cols = cols
        self.board = []
        self.square_size = height // rows
        self.caption = "Checkers"
        self.window_instance = pygame.display.set_mode((width,height))
        pygame.display.set_caption(self.caption)

    def update_piece_positions(self,board):
        self.board = board
    def add_squares(self):
        self.window_instance.fill(BLACK)

        for row in range(self.rows):
            #start= row%2 -> if row is 0 (0%2 = 0, we start from o)
            #             -> if row is 1 (1%2 = 0, we start from 1)
            #end = rows, which is 8
            #move by multiples of two for each iteration
            for col in range(row % 2, self.rows, 2):
                #starting from the top left
                #width of board = we draw 8 squares for the row
                #height of board = we draw 8 squares for the column
                #this creates the initial empty grid
                pygame.draw.rect(self.window_instance, WHITE, (row * self.square_size, col * self.square_size, self.square_size,self.square_size ))

    def add_pieces(self):
        circle_size = 15
        radius = self.square_size//2 - circle_size

        for row in self.board:
            for piece in row:
                if piece == 0:
                    pass
                else:
                    square_width_center = (piece.col * self.square_size) + self.square_size//2
                    square_height_center = (piece.row * self.square_size) + self.square_size//2
                    fill_color = piece.color
                    if piece.king == True:
                        fill_color = GREY if piece.color == "WHITE" else PINK

                    pygame.draw.circle(self.window_instance,fill_color,(square_width_center,square_height_center),radius )

    def create_board(self,new_board):
        self.update_piece_positions(new_board)
        self.add_squares()
        self.add_pieces()


# class BoardPiece:
#     def __init__(self,width,height,is_king,color):
#         pass


    
# def main(list_board):
#     pygame_board = PyGameBoard(list_board)
#     #board.create_board()
#     run_window(list_board,pygame_board)

# def run_window(list_board,visual_board):
#     clock = pygame.time.Clock()
#     running = True
#     while running:
#         clock.tick(60)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             # elif event.type == pygame.TEXTINPUT:
#             #     game.board()
#             visual_board.create_board()
#             pygame.display.update()

#main()