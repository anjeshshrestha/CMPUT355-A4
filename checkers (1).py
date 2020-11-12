import pygame

#set the width and height of the window
screen_width = 1000
screen_height = 1000
#set the # of rows and columns
rows = 8
columns = 8
#size of one square on the grid
one_square_size = screen_height//rows
#colours (rgb)
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
grey = (128,128,128)


#set up the screen
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("CHECKERS")

class make_board:
    def __init__(self):
        self.board = []
        self.white_pieces_left = 12
        self.red_pieces_left = 12
        self.white_kings = 0
        self.red_kings = 0
        self.create_board()

        

    def add_squares(self,screen):
        #add the squares on the board

        #start by making the whole screen black
        screen.fill(black)


        for row in range(rows):
            #start= row%2 -> if row is 0 (0%2 = 0, we start from o)
            #             -> if row is 1 (1%2 = 0, we start from 1)
            #end = rows, which is 8
            #move by multiples of two for each iteration
            for col in range(row % 2, rows, 2):
                #starting from the top left
                #width of board = we draw 8 squares for the row
                #height of board = we draw 8 squares for the column
                #this creates the initial empty grid
                pygame.draw.rect(screen, white, (row * one_square_size, col * one_square_size, one_square_size,one_square_size ))

    def create_board(self):
        self.add_squares(screen)
        for row in range(rows):
            #so we have an empty list for each row
            self.board.append([])
            for col in range(columns):
                #find out which column/row to draw on
                #alternating between every row, draw a piece in every other square
                if row < 3:
                    if row % 2 != col % 2:
                        self.board[row].append(checker_pieces(row,col,white))
                        self.board[row][col].draw_piece(screen)
                    else:
                        self.board[row].append(0)
                elif row > 4:
                    if row % 2 != col % 2:
                        self.board[row].append(checker_pieces(row,col,red))
                        #add checkers piece
                        self.board[row][col].draw_piece(screen)
                        #if no piece in that pos, we set it to 0
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)


class checker_pieces:

    circle_size =   15

    def __init__(self,row, column, colour):
        self.row = row
        self.column = column
        self.colour = colour

        self.square_width_center = 0
        self.square_height_center = 0
    
    def draw_piece(self,screen):
        #finds the center of the square of the current square we're in so we can draw the circle piece from there so it is centered
        self.square_width_center = (self.column * one_square_size) + one_square_size//2
        self.square_height_center = (self.row * one_square_size) + one_square_size//2

        radius = one_square_size//2 - self.circle_size
        pygame.draw.circle(screen,self.colour,(self.square_width_center,self.square_height_center),radius )


def main():
    game_playing = True

    #rate game runs at
    clock = pygame.time.Clock()
    board = make_board()


    while game_playing == True:

        clock.tick(60)

        #check if any events have happened
        for event in pygame.event.get():

            #if event type is quit, exit from while loop
            if event.type == pygame.QUIT:
                game_playing = False

            
            board.create_board()
            pygame.display.update()



            
                
    


        
       
        
    pygame.quit()

main()