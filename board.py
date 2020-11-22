from piece import Piece
# assume player 1 is white
# assume player 2 is red
class Board:
    def __init__(self):
        self.board = []
        self.moves = []
        self.player = 1
        self.rows = 8
        self.cols = 8

        self.playerColor = ["","WHITE", "RED"]
        self.playerColorShort = [".","w", "r"]
        self.playerColorKing = [".","W", "R"]

        self.player1Pieces = []
        self.player1PieceCount = 12
        self.player2Pieces = []
        self.player2PieceCount = 12
        self.create_board()
    
    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(self.rows):
            self.board.append([])
            for col in range(self.cols):
                if col % 2 == ((row +  1) % 2):
                    if row < 3: #top half - player 1
                        temp_piece = Piece(row, col, self.playerColor[1], self.playerColorShort[1], self.playerColorKing[1])
                        self.board[row].append(temp_piece)
                        self.player1Pieces.append(temp_piece)
                    elif row > 4: #bottom half - player 2
                        temp_piece = Piece(row, col, self.playerColor[2], self.playerColorShort[2], self.playerColorKing[2])
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
        print()


    #check who's turn it is to play
    def whose_turn(self):
        return self.player

    #check to see if there is a winner
    def has_winner(self):
        return self.player1PieceCount == 0 or self.player2PieceCount == 0
    
    #if there is no more pieces left return who won
    def get_winner(self):
        if self.player2PieceCount == 0:
            return "Player 1 is Winner"
        elif self.player1PieceCount == 0:
            return "Player 2 is Winner"
        
    #given a move (current posititon, list of pieces with moves, index of piece, index of move)
    #will make the move, capture any piece in the way
    # given example:
    #        curPOS   newPOS   no-capture
    # WHITE: (3, 0) : {(4, 1): []}
    #        curPOS    newPOS     capture     newPOS     capture    catpure       newPOS  no-capture
    # WHITE: (2, 5) : {(4, 3): [RED: (3, 4)], (6, 1): [RED: (5, 2), RED: (3, 4)], (3, 6): []}
    def make_move(self, moves, piece, index_move):
        moves = moves[piece]
        new_place = list(moves.keys())[index_move]
        captures = moves[new_place]
        print(piece, "," ,new_place, "," ,captures)
        self.move(piece, new_place, captures)
        
    #move a piece from before to after
    def move(self,piece, new_place, captures):
        row,col = new_place
        #set old position to free
        self.board[piece.row][piece.col] = 0
        #move the piece in pieces
        piece.move(row,col)
        #set new location to current piece
        self.board[row][col] = piece

        #capture pieces
        self.capture(captures)

        #make it king if at end
        if self.player == 1 and row == self.rows-1:
            piece.make_king()
        elif self.player == 2 and row == 0:
            piece.make_king()
        
        #record the move
        self.moves.append([(piece.row,piece.col),new_place, captures])

        #change turns
        self.change_turn()
    def capture(self,captures):
        for piece in captures:
            self.board[piece.row][piece.col] = 0
            piece.capture()
            print("Captured", piece)
            if self.player == 1:
                self.player2PieceCount -= 1
            elif self.player == 2:
                self.player1PieceCount -= 1
            
    #change turn of play, should be called from move
    def change_turn(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def print_all_valid_moves(self):
        temp = self.get_all_valid_moves()
        count = 0
        for piece, moves in temp.items():
            print(count, " : ", piece,":",moves)
            count += 1
        return temp
    
    #itterate over all pieces of player that is not captured
    #find moves it can make and save it a list
    #return list
    def get_all_valid_moves(self):
        all_moves = {}
        if self.player == 1:
            for piece in self.player1Pieces:
                if not piece.captured:
                    temp = self.get_valid_moves(piece)
                    if temp != {}:
                        all_moves[piece] = temp
        else:
            for piece in self.player2Pieces:
                if not piece.captured:
                    temp = self.get_valid_moves(piece)
                    if temp != {}:
                        all_moves[piece] = temp
        return all_moves

    #given a piece find position it can move to
    #find places it can move to - an right
    # https://github.com/techwithtim/Python-Checkers/blob/master/checkers/board.py
    # after spending too much time, trying to implement own method to multiple capture
    # using algoritm from above to find valid move and captures
    def get_valid_moves(self,piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        if piece.color == "RED" or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == "WHITE" or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, self.rows), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, self.rows), 1, piece.color, right))
    
        return moves

    def _traverse_left(self, start_row, stop_row, direction, color, left_col, skipped=[]):
        moves = {}
        last = []
        for cur_row in range(start_row, stop_row, direction):
            if left_col < 0:
                break
            
            current = self.board[cur_row][left_col]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(cur_row, left_col)] = last + skipped
                else:
                    moves[(cur_row, left_col)] = last
                
                if last:
                    if direction == -1:
                        row = max(cur_row-3, 0)
                    else:
                        row = min(cur_row+3, self.rows)
                    moves.update(self._traverse_left(cur_row+direction, row, direction, color, left_col-1,skipped=last))
                    moves.update(self._traverse_right(cur_row+direction, row, direction, color, left_col+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left_col -= 1
        
        return moves
   

    def _traverse_right(self, start_row, stop_row, direction, color, right_col, skipped=[]):
        moves = {}
        last = []
        for cur_row in range(start_row, stop_row, direction):
            if right_col >= self.cols:
                break
            
            current = self.board[cur_row][right_col]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(cur_row,right_col)] = last + skipped
                else:
                    moves[(cur_row, right_col)] = last
                
                if last:
                    if direction == -1:
                        row = max(cur_row-3, 0)
                    else:
                        row = min(cur_row+3, self.rows)
                    moves.update(self._traverse_left(cur_row+direction, row, direction, color, right_col-1,skipped=last))
                    moves.update(self._traverse_right(cur_row+direction, row, direction, color, right_col+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right_col += 1
        
        return moves
    


def main():
    board = Board()
    board.print_board()

    while not board.has_winner():
        #white
        print("Player:",board.whose_turn())
        x_temp = board.print_all_valid_moves()
        while True:
            abc = int(input("piece index: "))
            if abc < len(x_temp):
                break
        y_piece = list(x_temp.keys())[abc]
        while True:
            cdf = int(input("piece move: "))
            if cdf < len(list(x_temp[y_piece].keys())):
                break
        board.make_move(x_temp,y_piece, cdf)
        board.print_board()
    
main()
