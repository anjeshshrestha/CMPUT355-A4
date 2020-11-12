from piece import Piece
# assume player 1 is white
# assume player 2 is red
class Board:
    def __init__(self):
        self.board = []
        self.moves = []
        self.player = 2
        self.rows = 8
        self.cols = 8

        self.player1Color = "white"
        self.player1ColorShort = "w"
        self.player1ColorKing = "W"
        self.player1Pieces = []

        self.player2Color = "red"
        self.player2ColorShort = "r"
        self.player2ColorKing = "R"
        self.player2Pieces = []

    
    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(self.rows):
            self.board.append([])
            for col in range(self.cols):
                if col % 2 == ((row +  1) % 2):
                    if row < 3: #top half - player 1
                        temp_piece = Piece(row, col, self.player1Color, self.player1ColorShort, self.player1ColorKing)
                        self.board[row].append(temp_piece)
                        self.player1Pieces.append(temp_piece)
                    elif row > 4: #bottom half - player 2
                        temp_piece = Piece(row, col, self.player2Color, self.player2ColorShort, self.player2ColorKing)
                        self.board[row].append(temp_piece)
                        self.player2Pieces.append(temp_piece)
                    else:
                        self.board[row].append(0)
                   
                else:
                    self.board[row].append(0)

    #print board with padding of nubers
    def print_board(self):
        print("   0 1 2 3 4 5 6 7")
        print("   _______________")
        for row in range(self.rows):
            print(row,end="| ")
            for col in range(self.cols):
                if self.board[row][col] == 0:
                    print(". ", end="")
                elif self.board[row][col].king:
                    print(self.board[row][col].colorKing, end=" ")
                else:
                    print(self.board[row][col].colorShort, end=" ")
            print("")
    
    #move a piece from before to after
    # needs:
    # clean up
    # check if move is valid
    # check if correct player piece is moving (white is moving white)
    def move(self,row,col, new_row,new_col):
        temp_piece = self.board[row][col]
        
        self.board[row][col] = 0
        self.board[new_row][new_col] = temp_piece
        temp_piece.move(new_row,new_col)
        self.moves.append([(row,col),(new_row,new_col)])

        self.change_turn()

    #change turn of play, should be called from move
    def change_turn(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    #return if speicied position is valid
    # no longer need i think
    def valid_position(self, row, col):
        return (row >= 0 and row <= self.rows) and (col >= 0 and col <= self.cols)

    #check who's turn it is to play
    def whose_turn(self):
        return self.player

    #check to see if there is a winner
    def has_winner(self):
        return len(self.player2Pieces) == 0 or len(self.player2Pieces) == 0
    
    #if there is no more pieces left return who won
    def get_winner(self):
        if len(self.player2Pieces) == 0:
            return "Player 1 is Winner"
        elif len(self.player2Pieces) == 0:
            return "Player 2 is Winner"

    def get_all_valid_moves(self):
        all_moves = []
        if self.player == 1:
            for piece in self.player1Pieces:
                all_moves.extend(self.get_valid_moves(self.player,piece.row, piece.col, piece.color))
        else:
            for piece in self.player2Pieces:
                all_moves.extend(self.get_valid_moves(self.player,piece.row, piece.col, piece.color))
        return all_moves

    #given a piece find position it can move to
    def get_valid_moves(self,player,row,col, color):
        piece = self.board[row][col]
        if piece == 0:
            return ["not a valid piece"]
        moves = []

        if player == 1 or piece.is_king():
            moves.extend(self._lookLeft("down",row, col,color)) #top piece move down
            moves.extend(self._lookRight("down",row, col,color)) #top piece move down

        if player == 2 or piece.is_king():
            moves.extend(self._lookLeft("up",row, col,color)) #bottom piece move up
            moves.extend(self._lookRight("up",row, col,color)) #bottom piece move up
        
        if moves != []:
            return [([row,col],moves)]
        return []


    #seraches down left side of the board from given location
    #direction is where the piece will be moving towards
    #when it encounters a piece, not its own color, 
    #          check if it can to a empty spot after captring
    #   (need to implement recursive capturing)
    # -----in progress capture
    # after getting back where it can move, call get_valid_moves to recurse
    
    def _lookLeft(self,direction,given_row,given_col,color, needEmpty = False):
        new_places = []
        if direction == "up" or direction == "king":
            if given_row-1 >= 0 and given_col-1 >= 0:
                new_places.append((given_row-1,given_col-1)) #top left
        if direction == "down" or direction == "king":
            if given_row+1 < self.rows and given_col-1 >= 0:
                new_places.append((given_row+1,given_col-1)) #bottom left

        valid_places = []
        check_capture = []
        for row,col in new_places:
            if self.board[row][col] == 0:
                valid_places.append((row,col))
            else:
                if not needEmpty and self.board[row][col].color != color:
                    check_capture.append((row,col))
        
        for row,col in check_capture:
            valid_places.extend(self._lookLeft(direction,row,col,color, True))

        return valid_places

    def _lookRight(self,direction,given_row,given_col,color,needEmpty = False):
        new_places = []
        if direction == "up" or direction == "king":
            if given_row-1 >= 0 and given_col+1 < self.cols:
                new_places.append((given_row-1,given_col+1)) #top right
        if direction == "down" or direction == "king":
            if given_row+1 < self.rows and given_col+1 < self.cols:
                new_places.append((given_row+1,given_col+1)) #bottom right

        valid_places = []
        check_capture = []
        for row,col in new_places:
            if self.board[row][col] == 0:
                valid_places.append((row,col))
            else:
                if not needEmpty and self.board[row][col].color != color:
                    check_capture.append((row,col))

        for row,col in check_capture:
            valid_places.extend(self._lookRight(direction,row,col,color,True))

        return valid_places
    
    def make_move(self,move,index):
        if len(move) != 2:
            return
        
        row,col = move[0]
        new_row,new_col = move[1][index]

        piece = self.board[row][col]
        
        if abs(row-new_row) >1 or abs(col-new_col) > 1:
            print("---------------------------")
            print("Capturing")
            mid_row = (new_row+row)//2
            mid_col = (new_col+col)//2
            print(mid_row,mid_col )
            remove_piece = self.board[mid_row][mid_col]
            remove_piece.capture()
            self.board[mid_row][mid_col] = 0
            print("---------------------------")


        #add to check if piece in way and have to capture

        self.move(row,col,new_row,new_col)

def main():
    board = Board()
    board.create_board()
    board.print_board()


    #red
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    print(x)
    board.make_move(x[0],0)
    board.print_board()
    print()
    
    #white
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    print(x)
    board.make_move(x[0],1)
    board.print_board()

    #red
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    print(x)
    board.make_move(x[-3],1)
    board.print_board()
    print()

    #white
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    print(x)
    
    board.make_move(x[2],0)
    board.print_board()

    '''
    #move red to just below white
    print("red")
    x = board.get_valid_moves(5,2)
    print(x)
    board.move(5,2,4,1)
    board.print_board()
    
    print("red")
    x = board.get_valid_moves(4,1)
    print(x)
    board.move(4,1,3,2)
    board.print_board()

    print("red")
    x = board.get_valid_moves(3,2)
    print(x)

    #see white capture moves
    print("white")
    y = board.get_valid_moves(2,1)
    print(y)
    '''

main()