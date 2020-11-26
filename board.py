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
        self.player1PiecesCount = 0
        self.player2Pieces = []
        self.player2PiecesCount = 0
        #self.create_board()

    #returns a piece on the board
    def get_piece(self, row, col):
        return self.board[row][col]
    
    #creates the starting of board
    def create_board(self):
        for row in range(self.rows):
            self.board.append([])
            for col in range(self.cols):
                if col % 2 == ((row +  1) % 2):
                    if row < 3: #top half - player 1
                        temp_piece = Piece(row, col, self.playerColor[1], self.playerColorShort[1], self.playerColorKing[1])
                        self.board[row].append(temp_piece)
                        self.player1Pieces.append(temp_piece)
                        self.player1PiecesCount += 1
                    elif row > 4: #bottom half - player 2
                        temp_piece = Piece(row, col, self.playerColor[2], self.playerColorShort[2], self.playerColorKing[2])
                        self.board[row].append(temp_piece)
                        self.player2Pieces.append(temp_piece)
                        self.player2PiecesCount += 1
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
        return self.player1PiecesCount == 0 or self.player2PiecesCount == 0
    
    #if there is no more pieces left return who won
    def get_winner(self):
        if self.player1PiecesCount == 0:
            return "Player 1 is Winner"
        elif self.player2PiecesCount == 0:
            return "Player 2 is Winner"

    #itterate over all pieces of player that is not captured
    #find moves it can make and save it a list
    #if a piece can capture, only return moves of pieces that can capture
    #return dictionary
    # { (x,y) : [[(x,y),(a,b)],[(x,y),(g,d),(f,h)]]
    #   ....
    # }
    def get_all_valid_moves(self):
        all_moves = {}
        all_capture_moves = {}
        print("aaa1")
        if self.player == 1:
            for piece in self.player1Pieces:
                if not piece.captured:
                    print("aaa3")
                    capture, temp = self.get_valid_moves(piece)
                    print("aaa7")
                    if capture:
                        all_capture_moves[(piece.row, piece.col)] = temp
                    elif temp != []:
                        all_moves[(piece.row, piece.col)] = temp
        else:
            for piece in self.player2Pieces:
                if not piece.captured:
                    print("aaa3")
                    capture, temp = self.get_valid_moves(piece)
                    print("aaa7")
                    if capture:
                        all_capture_moves[(piece.row, piece.col)] = temp
                    if temp != []:
                        all_moves[(piece.row, piece.col)] = temp
        print("aaa8")
        if all_capture_moves != {}:
            print("aaa9")
            return all_capture_moves
        else:
            print("aaa10")
            return all_moves
        
    #print all moves a piece can make
    def print_all_valid_moves(self):
        temp = self.get_all_valid_moves()
        for piece, moves in temp.items():
            print(piece, moves)
        return temp
    
    #given a piece find position it can move to
    #find places it can move to
    #if it can capture, return capture move only
    def get_valid_moves(self,piece):
        moves = []
        list_of_places = []
        #check for emptty space
        if piece.king or self.player==1: # look moving down
            if piece.row+1 < self.rows and piece.col+1 < self.cols and self.board[piece.row+1][piece.col+1] == 0: #right
                moves.append([(piece.row,piece.col),(piece.row+1,piece.col+1)])
            if piece.row+1 < self.rows and piece.col-1 >= 0 and self.board[piece.row+1][piece.col-1] == 0:#left
                moves.append([(piece.row,piece.col),(piece.row+1,piece.col-1)])
        if piece.king or self.player==2: # look moving up
            if piece.row-1 >= 0 and piece.col+1 < self.cols and self.board[piece.row-1][piece.col+1] == 0:#right
                moves.append([(piece.row,piece.col),(piece.row-1,piece.col+1)])
            if piece.row-1 >= 0 and piece.col-1 >= 0 and self.board[piece.row-1][piece.col-1] == 0: #left
                moves.append([(piece.row,piece.col),(piece.row-1,piece.col-1)])
        print("aaa4")
        #check for capture pieces
        check_capture_list = [(piece.row,piece.col)]
        tempo_dict = {}
        while len(check_capture_list) !=0:
            row,col = check_capture_list.pop()
            new_check = self.can_capture(piece,row,col)
            for new in new_check:
                if new not in tempo_dict:
                    check_capture_list.append(new)
            #check_capture_list.extend(new_check)
            if new_check:
                if (row,col) not in tempo_dict:
                    tempo_dict[(row,col)] = []
                    print("HERER----------------------", tempo_dict, new_check)
                    if new_check[0] not in tempo_dict[(row,col)]:
                        tempo_dict[(row,col)].extend(new_check)
            print("aaa5", check_capture_list)
        if list(tempo_dict):
            last_key = list(tempo_dict)[-1]
            if not tempo_dict[last_key]:
                print("last key",tempo_dict[last_key])
                print("something1",list(tempo_dict))
                del tempo_dict[last_key]
                print("something2",list(tempo_dict))

        print("aaa6")
        x = self.dfs((piece.row,piece.col),[],tempo_dict,[])

        ### un-nest the x
        temp_moves = []
        if (piece.row,piece.col) not in x:
            print(x)
            for y in x:
                temp_moves.append(self.get_unNested(y))
            print("aaa66")
        if temp_moves != []:
            print(temp_moves)
            return (True, temp_moves)
        else:
            return (False, moves)
        
    #unnest a nested list [[1,2,3]] -> [1,2,3]
    def get_unNested(self,alist):
        if len(alist) == 1:
            return self.get_unNested(alist[0])
        else:
            return alist
        
    #checks if it can capture a piece next to it and jump to a empty spot
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

    #return a sequence of moves for capture from a graph/tree
    def dfs(self,node,visited,graph,path):
        temp = []
        if node not in visited:
            if node not in graph or graph[node] == []:
                visited.append(node)
                path.append(node)
                return path
            else:
                visited.append(node)
                path.append(node)
                for x in graph[node]:
                    temp.append(self.dfs(x,visited,graph,path.copy()))
        return temp
    
    #handles sequence of moves and capturing 
    def make_moves(self, moves):
        print(moves)
        cur_row,cur_col = moves[0]
        for new_row, new_col in moves[1:]:
            print("Moving",self.playerColorShort[self.player], "From", (cur_row,cur_col), "to", (new_row,new_col))
            #move the piece
            self.move(cur_row,cur_col,new_row,new_col)
            
            #condition check to see if there is piece in the way we have to capture
            if abs(cur_row-new_row) > 1 or abs(cur_col-new_col) > 1:
                mid_row = (new_row+cur_row)//2
                mid_col = (new_col+cur_col)//2
                print("!!! Capturing", (mid_row,mid_col))
                remove_piece = self.board[mid_row][mid_col]
                remove_piece.capture()
                self.board[mid_row][mid_col] = 0
                if self.player == 1:
                    self.player2PiecesCount -= 1
                elif self.player == 2:
                    self.player1PiecesCount -= 1
            cur_row,cur_col = new_row,new_col
        #change turns
        self.change_turn()

    #make move with most captures or first found
    def get_best_move(self,moves):
        best = -1
        best_move = None
        for piece, move in moves.items():
            for sequence in move:
                if len(sequence) > best:
                    best = len(sequence)
                    best_move = sequence
        return best_move

def main():
    board = Board()
    #prints the board
    board.print_board()
    #gets all moves
    # { (x,y) : [[(x,y),(a,b)],[(x,y),(g,d),(f,h)]]
    # ...
    # }
    
    x_temp = board.get_all_valid_moves()
    #print all moves
    board.print_all_valid_moves()
    #print(x_temp)  #uncomment this to see what the valid moves return
    #basically selects a move
    selected_move = board.get_best_move(x_temp)
    #passes the selected move to move the piece
    board.make_moves(selected_move)

    """
    while not board.has_winner():
        board.print_board()
        print("Player:",board.whose_turn())
        x_temp = board.print_all_valid_moves()
        print("Get best move: 1")
        print("Make move: 2")
        x = int(input())
        if x_temp == {}:
            print("Stalemate")
            break
        if x == 1:
            print(board.get_best_move(x_temp))
            print("Make best move: 1")
            print("Make move: 2")
            x = int(input())
            if x == 1:
                board.make_moves(board.get_best_move(x_temp))
            else:
                continue
        if x == 2:
            y = int(input("piece to move, positon row: "))
            z = int(input("piece to move, positon col: "))
            if (y,z) not in x_temp:
                continue
            
            print(x_temp[(y,z)])
            zz = int(input("sequence to make: "))
            if zz >= len(x_temp[(y,z)]):
                continue
            print(x_temp[(y,z)][zz])
            board.make_moves(x_temp[(y,z)][zz])
        print("---------------------------------------")
    print(board.get_winner())
    """
#main()

