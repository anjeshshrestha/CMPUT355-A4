from sys import flags
from piece import Piece

class Board:
    def __init__(self):
        self.board = None
        self.moves = None
        self.topPlayerPieces = None
        self.bottomPlayerPieces = None
        self.player = None
        self.rows = 8
        self.cols = 8
        self.topPlayerColor = "white"
        self.topPlayerColorShortCode = "w"
        self.bottomPlayerColor = "red"
        self.bottomPlayerColorShortCode = "r"
        self.create_board()

    
    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        self.board = []
        self.moves = []
        self.topPlayerPieces = []
        self.bottomPlayerPieces = []
        self.player = self.topPlayerColor
        for row in range(self.rows):
            self.board.append([])
            for col in range(self.cols):
                if col % 2 == ((row +  1) % 2):
                    if row < 3: #top half
                        temp_piece = Piece(row, col, self.topPlayerColor)
                        self.board[row].append(temp_piece)
                        self.topPlayerPieces.append(temp_piece)
                        #print(row, col, temp_piece.get_color())
                    elif row > 4: #bottom half
                        temp_piece = Piece(row, col, self.bottomPlayerColor)
                        self.board[row].append(temp_piece)
                        self.bottomPlayerPieces.append(temp_piece)
                        #print(row, col, temp_piece.get_color())
                    else:
                        self.board[row].append(0)
                   
                else:
                    self.board[row].append(0)


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

    def make_king(self,piece):
        piece.make_king()
    
    def move(self, old_row, old_col, new_row, new_col):
        temp_piece = self.board[old_row][old_col]
        self.board[old_row][old_col] = 0
        self.board[new_row][new_col] = temp_piece
        temp_piece.move(new_row,new_col)
        self.moves.append([(old_row,old_col),(new_row,new_col)])
        self.change_turn()

    def undo_move(self):
        # Undo the last move
        move = self.moves.pop()
        return

    def valid_moves(self, row, col):
        pass

    def change_turn(self):
        if self.player == self.topPlayerColor:
            self.player = self.bottomPlayerColor
        else:
            self.player = self.topPlayerColor

    def valid_position(self, row, col):
        return (row >= 0 and row <= self.rows) and (col >= 0 and col <= self.cols)

    def whose_turn(self):
        return self.player

    def has_winner(self):
        return len(self.topPlayerPieces) == 0 or len(self.bottomPlayerPieces) == 0
    
    def get_winner(self):
        if len(self.topPlayerPieces) == 0:
            return "bottom"
        elif len(self.bottomPlayerPieces) == 0:
            return "top"

    def get_legal_moves(self):
        # Get legal moves for player to play
        if self.player == self.topPlayerColor:
            pieces = self.topPlayerPieces
        else:
            pieces = self.bottomPlayerPieces

        moves = []
        for piece in pieces:
            moves_for_piece = self.get_valid_moves_for_piece(piece)
            if len(moves_for_piece) > 0:
                moves.append(moves_for_piece)

        return moves

    def get_valid_moves_for_piece(self, piece):
        moves = []
        if piece.get_color() == self.bottomPlayerColor or piece.king:
            moves.extend(self._lookLeft("up",piece.get_row(), piece.get_column(),piece.get_color())) #bottom piece look up
            moves.extend(self._lookRight("up",piece.get_row(), piece.get_column(),piece.get_color())) #bottom piece look up
        if piece.get_color() == self.topPlayerColor or piece.king:
            moves.extend(self._lookLeft("down",piece.get_row(), piece.get_column(),piece.get_color())) #top piece look down
            moves.extend(self._lookRight("down",piece.get_row(), piece.get_column(),piece.get_color())) #top piece look down
        
        return moves

    def _lookLeft(self,direction,given_row,given_col,color):
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
                if self.board[row][col].get_color() != color:
                    check_capture.append((row,col))
        
        for row,col in check_capture:
            continue
            valid_places.extend(self._lookLeft(direction,row,col,color))
            valid_places.extend(self._lookRight(direction,row,col,color))

        return valid_places
    def _lookRight(self,direction,given_row,given_col,color):
        new_places = []
        #  1 - 2
        #  - x -
        #  3 - 4
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
                if self.board[row][col].get_color() != color:
                    check_capture.append((row,col))

        for row,col in check_capture:
            continue
            valid_places.extend(self._lookLeft(direction,row,col,color))
            valid_places.extend(self._lookRight(direction,row,col,color))

        return valid_places
    
def main():
    board = Board()
    board.print_board()
    temp = board.board[5][2]
    x = board.get_valid_moves_for_piece(temp)
    print(x)
    board.move(temp.get_row(),temp.get_column(),4,1)
    board.print_board()
    
    x = board.get_valid_moves_for_piece(temp)

    print(x)
    board.move(temp.get_row(),temp.get_column(),3,2)
    board.print_board()
    x = board.get_valid_moves_for_piece(temp)
    print(x)

    temp2 = board.board[2][1]
    y = board.get_valid_moves_for_piece(temp2)
    print(y)

# Invoke main() if called via `python3 board.py`
# but not if `python3 -i board.py` or `from board import *`
if __name__ == '__main__' and not flags.interactive:
    main()