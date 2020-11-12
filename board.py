from piece import Piece
class Board:
    def __init__(self):
        self.board = None
        self.moves = None
        self.player = "white"
        self.rows = 8
        self.cols = 8

        self.topPlayerColor = "white"
        self.topPlayerColorShortCode = "w"
        self.topPlayerPieceCount = 12

        self.bottomPlayerColor = "red"
        self.bottomPlayerColorShortCode = "r"
        self.bottomPlayerPieceCount = 12

    
    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        self.board = []
        self.moves = []
        for row in range(self.rows):
            self.board.append([])
            for col in range(self.cols):
                if col % 2 == ((row +  1) % 2):
                    if row < 3: #top half
                        temp_piece = Piece(row, col, self.topPlayerColor)
                        self.board[row].append(temp_piece)
                        #print(row, col, temp_piece.get_color())
                    elif row > 4: #bottom half
                        temp_piece = Piece(row, col, self.bottomPlayerColor)
                        self.board[row].append(temp_piece)
                        #print(row, col, temp_piece.get_color())
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
                elif self.board[row][col].get_color() == self.topPlayerColor:
                    print(self.topPlayerColorShortCode, end=" ")
                elif self.board[row][col].get_color() == self.bottomPlayerColor:
                    print(self.bottomPlayerColorShortCode, end=" ")
            print("")
    
    #move a piece from before to after
    # needs:
    # clean up
    # check if move is valid
    # check if correct player piece is moving (white is moving white)
    def move(self,old_row,old_col, new_row,new_col):
        temp_piece = self.board[old_row][old_col]
        
        self.board[old_row][old_col] = 0
        self.board[new_row][new_col] = temp_piece
        temp_piece.move(new_row,new_col)
        self.moves.append([(old_row,old_col),(new_row,new_col)])

    #change turn of play, should be called from move
    def change_turn(self):
        if self.player == self.topPlayerColor:
            self.player = self.bottomPlayerColor
        else:
            self.player = self.topPlayerColor

    #return if speicied position is valid
    # no longer need i think
    def valid_position(self, row, col):
        return (row >= 0 and row <= self.rows) and (col >= 0 and col <= self.cols)

    #check who's turn it is to play
    def whose_turn(self):
        return self.player

    #check to see if there is a winner
    def has_winner(self):
        return len(self.topPlayerPieceCount) == 0 or len(self.bottomPlayerPieceCount) == 0
    
    #if there is no more pieces left return who won
    def get_winner(self):
        if len(self.topPlayerPieceCount) == 0:
            return "bottom"
        elif len(self.bottomPlayerPieceCount) == 0:
            return "top"
        return "none"

    #given a piece find position it can move to
    def get_valid_moves(self,row,col):
        piece = self.board[row][col]
        if piece == 0:
            return ["not a valid piece"]
        moves = []
        if piece.get_color() == self.bottomPlayerColor or piece.is_king():
            moves.extend(self._lookLeft("up",piece.get_row(), piece.get_column(),piece.get_color())) #bottom piece look up
            moves.extend(self._lookRight("up",piece.get_row(), piece.get_column(),piece.get_color())) #bottom piece look up
        if piece.get_color() == self.topPlayerColor or piece.is_king():
            moves.extend(self._lookLeft("down",piece.get_row(), piece.get_column(),piece.get_color())) #top piece look down
            moves.extend(self._lookRight("down",piece.get_row(), piece.get_column(),piece.get_color())) #top piece look down
        
        return moves


    #seraches down left side of the board from given location
    #direction is where the piece will be moving towards
    #when it encounters a piece, not its own color, 
    #          check if it can to a empty spot after captring
    #   (need to implement recursive capturing)
    # -----in progress
    #  capture looks like this 
    #  capture, peice location, move location
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
                if not needEmpty and self.board[row][col].get_color() != color:
                    check_capture.append((row,col))
        
        for row,col in check_capture:
            x = self._lookLeft(direction,row,col,color, True)
            if x != []:
                x.insert(0,(row,col))
                x.insert(0,"capture")
                valid_places.append(x)
            #valid_places.extend(self._lookRight(direction,row,col,color))

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
                if not needEmpty and self.board[row][col].get_color() != color:
                    check_capture.append((row,col))

        for row,col in check_capture:
            x = self._lookRight(direction,row,col,color,True)
            if x != []:
                x.insert(0,(row,col))
                x.insert(0,"capture")
                valid_places.append(x)

        return valid_places
    
def main():
    board = Board()
    board.create_board()
    board.print_board()

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

main()