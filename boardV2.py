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

    #itterate over all pieces of player that is not captured
    #find moves it can make and save it a list
    #return list
    def get_all_valid_moves(self):
        all_moves = {}
        if self.player == 1:
            for piece in self.player1Pieces:
                if not piece.captured:
                    temp = self.get_valid_moves(piece.row, piece.col, piece.color)
                    if temp != {'capture': [], 'non_capture': []}:
                        all_moves[(piece.row, piece.col)] = temp
        else:
            for piece in self.player2Pieces:
                if not piece.captured:
                    temp = self.get_valid_moves(piece.row, piece.col, piece.color)
                    if temp != {'capture': [], 'non_capture': []}:
                        all_moves[(piece.row, piece.col)] = temp
        return all_moves

    def print_all_valid_moves(self):
        temp = self.get_all_valid_moves()

        for piece, moves in temp.items():
            print(piece, moves)

    #given a piece find position it can move to
    #find places it can move to - an right
    def get_valid_moves(self,row,col, color):
        piece = self.board[row][col]
        moves = {'non_capture': [], 'capture':[]}
        if piece != 0:
            temp_left = self._lookLeft(row, col,row, col,color,{}) #player 1 move down
            temp_right = self._lookRight(row, col,row, col,color,{}) #player 1 move down
            
            moves.update(temp_left)
            
            if 'non_capture' in temp_right:
                moves['non_capture'].extend(temp_right['non_capture'])
                
            if 'capture' in temp_right:
                moves['capture'].extend(temp_right['capture'])

            
            if moves != {'non_capture': [], 'capture':[]}:
                return moves
        return moves


    #seraches down left side of the board from given location
    #direction is where the piece will be moving towards
    #when it encounters a piece, not its own color, 
    #          check if it can to a empty spot after captring
    #   (need to implement recursive capturing)
    # -----in progress capture
    # after getting back where it can move, call get_valid_moves to recurse
    
    def _lookLeft(self,start_row,start_col, cur_row, cur_col, color, valid_places, needEmpty = False):
        if 'capture' not in valid_places:
            valid_places['capture'] = []
        if 'non_capture' not in valid_places:
            valid_places['non_capture'] = []
        
        new_row = new_col = None
        #check the left side it can move to
        if self.player == 1 and cur_row+1 < self.rows and cur_col-1 >= 0:
            new_row = cur_row+1
            new_col = cur_col-1 #bottom left
        elif self.player == 2 and cur_row-1 >= 0 and cur_col-1 >= 0:
            new_row = cur_row-1
            new_col = cur_col-1 #top left
        else:
            return valid_places
                
        #check if there is empty piece or enemy piece in the way
        check_capture = False
        if self.board[new_row][new_col] == 0:
            #if checking for empty place after jumping
            if needEmpty:
                valid_places['capture'].append((new_row,new_col))
                #check for reJump
                left_copy = {}
                right_copy = {}
                left_copy = self._lookLeft(start_row,start_col, new_row, new_col, color,left_copy)
                right_copy = self._lookRight(start_row,start_col, new_row, new_col, color, right_copy)
                
                
                if left_copy != {'non_capture': [], 'capture':[]} and left_copy != {}:
                    print((start_row,start_col),"left:",left_copy)
                    left_copy['capture'].insert(0,(new_row,new_col))
                    valid_places['capture'].append(left_copy['capture'])
                if right_copy != {'non_capture': [], 'capture':[]} and right_copy != {}:
                    print((start_row,start_col),"right",right_copy)
                    right_copy['capture'].insert(0,(new_row,new_col))
                    valid_places['capture'].append(right_copy['capture'])
                #print(valid_places)
                
                
            else:
                valid_places['non_capture'].append([(start_row,start_col),(new_row,new_col)])
        elif not needEmpty and self.board[new_row][new_col].color != color:
            check_capture = True
        #if there is piece in the way, check if it can jump over to empty place
        if check_capture:
            self._lookLeft(start_row,start_col, new_row, new_col, color, valid_places, True)
            
        return valid_places

    def _lookRight(self,start_row,start_col, cur_row, cur_col, color, valid_places, needEmpty = False):
        if 'capture' not in valid_places:
            valid_places['capture'] = []
        if 'non_capture' not in valid_places:
            valid_places['non_capture'] = []
        new_row = new_col = None
        #check the right side it can move to
        if self.player == 1 and cur_row+1 < self.rows and cur_col+1 < self.cols:
            new_row = cur_row+1 
            new_col = cur_col+1 # bottom right
        elif self.player == 2 and cur_row-1 >= 0 and cur_col+1 < self.cols:
            new_row = cur_row-1
            new_col = cur_col+1 #top right
        else:
            return valid_places
        
        #check if there is empty piece or enemy piece in the way
        check_capture = False
        if self.board[new_row][new_col] == 0:
            if needEmpty:
                valid_places['capture'].append((new_row,new_col))
                #check for reJump
                #left_copy = dict(valid_places)
                #right_copy = dict(valid_places)
                #self._lookLeft(start_row,start_col, new_row, new_col, color, left_copy)
                #self._lookRight(start_row,start_col, new_row, new_col, color, right_copy)
                #print((start_row,start_col),"left:",left_copy)
                #print((start_row,start_col),"right",right_copy)
            else:
                valid_places['non_capture'].append([(start_row,start_col),(new_row,new_col)])
        elif not needEmpty and self.board[new_row][new_col].color != color:
            check_capture = True
        #if there is piece in the way, check if it can jump over to empty place
        if check_capture:
            self._lookRight(start_row,start_col, new_row, new_col, color, valid_places, True)

        return valid_places
    
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
    
    #white - left
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    board.print_all_valid_moves()
    board.make_non_capture_move(x[(2,1)],0)
    board.print_board()
    print()

    #red - right
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    board.print_all_valid_moves()
    board.make_non_capture_move(x[(5,2)],1)
    board.print_board()
    print()

    #white - left
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    board.print_all_valid_moves()
    board.make_non_capture_move(x[(1,0)],0)
    board.print_board()
    print()

    #red - right
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    board.print_all_valid_moves()
    board.make_non_capture_move(x[(4,3)],1)
    board.print_board()
    print()

    #white - left
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    board.print_all_valid_moves()
    board.make_non_capture_move(x[(0,1)],0)
    board.print_board()
    print()

    #red - right
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    board.print_all_valid_moves()
    board.make_non_capture_move(x[(6,1)],0)
    board.print_board()
    print()

    #white - right
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    board.print_all_valid_moves()
    board.make_non_capture_move(x[(2,1)],0)
    board.print_board()
    print()
    
    #red - right
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    board.print_all_valid_moves()
    board.make_non_capture_move(x[(5,4)],1)
    board.print_board()
    print()
    
    #white - right
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    board.print_all_valid_moves()
    board.make_non_capture_move(x[(1,0)],0)
    board.print_board()
    print()

    #red - right
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    board.print_all_valid_moves()
    board.make_non_capture_move(x[(4,5)],0)
    board.print_board()
    print()

    #white - right
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    board.print_all_valid_moves()
    board.make_non_capture_move(x[(3,0)],0)
    board.print_board()
    print()

    #red - right
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    board.print_all_valid_moves()
    board.make_non_capture_move(x[(6,3)],0)
    board.print_board()
    print()

    #white - right
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    board.print_all_valid_moves()
    board.make_non_capture_move(x[(2,1)],0)
    board.print_board()
    print()

    #red - right
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    board.print_all_valid_moves()
    board.make_non_capture_move(x[(5,6)],1)
    board.print_board()
    print()

    #white - right
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    board.print_all_valid_moves()
    board.make_non_capture_move(x[(1,2)],0)
    board.print_board()
    print()

     #red - right
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    board.print_all_valid_moves()
    board.make_non_capture_move(x[(6,5)],0)
    board.print_board()
    print()

    #white - right
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    board.print_all_valid_moves()
    

"""
    #red
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    print(x)
    board.make_move(x,0,0)
    board.print_board()
    print()
    
    #white
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    print(x)
    board.make_move(x,0,1)
    board.print_board()

    #red
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    print(x)
    board.make_move(x,2,1)
    board.print_board()
    print()

    #white
    print("Player:",board.whose_turn())
    x = board.get_all_valid_moves()
    print(x)
    
    board.make_move(x,2,0)
    board.print_board()
    """

main()
