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
        self.player2Pieces = []

    
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
        
    #move a piece from before to after
    # needs:
    # clean up
    # check if move is valid
    # check if correct player piece is moving (white is moving white)
    def move(self,row,col, new_row,new_col):
        piece = self.board[row][col]
        #move the piece in pieces
        piece.move(new_row,new_col)
        #set new location to current piece
        self.board[new_row][new_col] = piece
        #set old position to free
        self.board[row][col] = 0

        #make it king if at end
        if self.player == 1 and new_row == self.rows-1:
            piece.make_king()
        elif self.player == 2 and new_row == 0:
            piece.make_king()

        #record the move
        self.moves.append([(row,col),(new_row,new_col)])

        #change turns
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
        return (row >= 0 and row < self.rows) and (col >= 0 and col < self.cols)

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

    #itterate over all pieces of player that is not captured
    #find moves it can make and save it a list
    #return list
    def get_all_valid_moves(self):
        all_moves = {}
        if self.player == 1:
            for piece in self.player1Pieces:
                if not piece.captured:
                    temp = self.get_valid_moves(piece)
                    if temp != {'capture': [], 'non_capture': []}:
                        all_moves[(piece.row, piece.col)] = temp
        else:
            for piece in self.player2Pieces:
                if not piece.captured:
                    temp = self.get_valid_moves(piece)
                    if temp != {'capture': [], 'non_capture': []}:
                        all_moves[(piece.row, piece.col)] = temp
        return all_moves

    def print_all_valid_moves(self):
        temp = self.get_all_valid_moves()

        for piece, moves in temp.items():
            print(piece, moves)

        return temp
    #given a piece find position it can move to
    #find places it can move to - an right
    def get_valid_moves(self,piece):
        moves = {'capture':[],'non_capture': []}
        list_of_places = []
        #check for emptty space
        if piece.king or self.player==1: # look moving down
            if piece.row+1 < self.rows and piece.col+1 < self.cols:
                list_of_places.append((piece.row+1,piece.col+1)) #right
            if piece.row+1 < self.rows and piece.col-1 >= 0:
                list_of_places.append((piece.row+1,piece.col-1)) #left
        if piece.king or self.player==2: # look moving up
            if piece.row-1 >= 0 and piece.col+1 < self.cols:
                list_of_places.append((piece.row-1,piece.col+1)) #right
            if piece.row-1 >= 0 and piece.col-1 >= 0:
                list_of_places.append((piece.row-1,piece.col-1)) #left
                
        for row,col in list_of_places:
            temp_piece = self.board[row][col]
            if temp_piece == 0:
                moves['non_capture'].append((row,col))

        #check for capture pieces
        check_capture_list = [(piece.row,piece.col)]
        tempo_dict = {}
        while len(check_capture_list) !=0:
            row,col = check_capture_list.pop()
            new_check = self.can_capture(piece,row,col)
            check_capture_list.extend(new_check)
            if new_check:
                if (row,col) not in tempo_dict:
                    tempo_dict[(row,col)] = []
                tempo_dict[(row,col)].extend(new_check)
        moves['capture'].append(tempo_dict)
        return moves
    
    def can_capture(self,piece,row,col):
        temp = []
        if piece.king or self.player==1: # look moving down
            if row+1 < self.rows and col+1 < self.cols:
                if self.board[row+1][col+1] != 0 and self.board[row+1][col+1].color != piece.color and self.valid_position(row+2,col+2) and self.board[row+2][col+2] == 0:
                    temp.append((row+2,col+2)) #right
            if row+1 < self.rows and col-1 >= 0:
                if self.board[row+1][col-1] != 0 and self.board[row+1][col-1].color != piece.color and self.valid_position(row+2,col-2) and self.board[row+2][col-2] == 0:
                    temp.append((row+2,col-2))#left
        if piece.king or self.player==2: # look moving up
            if row-1 >= 0 and col+1 < self.cols:
                if self.board[row-1][col+1] != 0 and self.board[row-1][col+1].color != piece.color and self.valid_position(row-2,col+2) and self.board[row-2][col+2] == 0:
                    temp.append((row-2,col+2))#right
            if row-1 >= 0 and col-1 >= 0:
                if self.board[row-1][col-1] != 0 and self.board[row-1][col-1].color != piece.color and self.valid_position(row-2,col-2) and self.board[row-2][col-2] == 0:
                    temp.append((row-2,col-2))#left
        return temp


    def move(self,old_row,old_col,new_row,new_col):
        piece = self.board[old_row][old_col]
        #set old position to free
        self.board[old_row][old_col] = 0
        #move the piece in pieces
        piece.move(new_row,new_col)
        #set new location to current piece
        self.board[new_row][new_col] = piece

        #make it king if at end
        if self.player == 1 and new_row == self.rows-1:
            piece.make_king()
        elif self.player == 2 and new_row == 0:
            piece.make_king()
        

        #change turns
        self.change_turn()
    
    #given a move (current posititon, list of pieces with moves, index of piece, index of move)
    #will make the move, capture any piece in the way
    # given example:
    #                   cur       new
    # {'non_capture': [[(6, 5), (5, 6)]], 'capture': []}
    def make_non_capture_move(self, moves, index_move):
        moves = moves['non_capture']
        #get current piece location and move location
        selected_move = moves[index_move]
        cur_row,cur_col = selected_move[0]
        new_row,new_col = selected_move[1]

        print("Moving",self.playerColorShort[self.player], "From", (cur_row,cur_col), "to", (new_row,new_col))
        #move the piece
        self.move(cur_row,cur_col,new_row,new_col)
        """

        #condition check to see if there is piece in the way we have to capture
        if abs(row-new_row) >1 or abs(col-new_col) > 1:
            mid_row = (new_row+row)//2
            mid_col = (new_col+col)//2
            print("!!! Capturing", (mid_row,mid_col))
            remove_piece = self.board[mid_row][mid_col]
            remove_piece.capture()
            self.board[mid_row][mid_col] = 0
            """
        
        

def main():
    board = Board()
    board.create_board()
    board.print_board()
    
    #white
    print("Player:",board.whose_turn())
    x = board.print_all_valid_moves()
    board.move(2,1,3,2)
    board.print_board()
    print()

    #red
    print("Player:",board.whose_turn())
    x = board.print_all_valid_moves()
    board.move(5,4,4,3)
    board.print_board()
    print()

    #white
    print("Player:",board.whose_turn())
    x = board.print_all_valid_moves()
    board.move(3,2,2,1)
    board.print_board()
    print()

    #red
    print("Player:",board.whose_turn())
    x = board.print_all_valid_moves()
    board.move(4,3,3,2)
    board.print_board()
    print()

    #white
    print("Player:",board.whose_turn())
    x = board.print_all_valid_moves()
    board.move(2,7,3,6)
    board.print_board()
    print()

    #red
    print("Player:",board.whose_turn())
    x = board.print_all_valid_moves()
    board.move(6,5,5,4)
    board.print_board()
    print()

    #white
    print("Player:",board.whose_turn())
    x = board.print_all_valid_moves()
    board.move(3,6,2,7)
    board.print_board()
    print()
    
#red
    print("Player:",board.whose_turn())
    x = board.print_all_valid_moves()
    board.move(6,1,1,1)
    board.print_board()
    print()
    #white
    
    print("Player:",board.whose_turn())
    x = board.print_all_valid_moves()
 
main()
