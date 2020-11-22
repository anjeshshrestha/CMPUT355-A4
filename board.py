from piece import Piece


TOPLEFT = 0
TOPRIGHT = 1
BOTTOMLEFT = 2
BOTTOMRIGHT = 3

# assume player 1 is white
# assume player 2 is red
class Board:
    def __init__(self):
        self.board = []
        self.moves = []
        self.player = 2
        self.rows = 8
        self.cols = 8

        self.playerColor = ["", "WHITE", "RED"]
        self.playerColorShort = [".", "w", "r"]
        self.playerColorKing = [".", "W", "R"]

        self.player1Pieces = []
        self.player2Pieces = []

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(self.rows):
            self.board.append([])
            for col in range(self.cols):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:  # top half - player 1
                        temp_piece = Piece(row, col, self.playerColor[1], self.playerColorShort[1],
                                           self.playerColorKing[1])
                        self.board[row].append(temp_piece)
                        self.player1Pieces.append(temp_piece)
                    elif row > 4:  # bottom half - player 2
                        temp_piece = Piece(row, col, self.playerColor[2], self.playerColorShort[2],
                                           self.playerColorKing[2])
                        self.board[row].append(temp_piece)
                        self.player2Pieces.append(temp_piece)
                    else:
                        self.board[row].append(0)

                else:
                    self.board[row].append(0)

    # print board with padding of nubers
    def print_board(self):
        print("   0 1 2 3 4 5 6 7")
        print("   _______________")
        for row in range(self.rows):
            print(row, end="| ")
            for col in range(self.cols):
                if self.board[row][col] == 0:
                    print(". ", end="")
                elif self.board[row][col].king:
                    print(self.board[row][col].colorKing, end=" ")
                else:
                    print(self.board[row][col].colorShort, end=" ")
            print("")
        print()

    # move a piece from before to after
    # needs:
    # clean up
    # check if move is valid
    # check if correct player piece is moving (white is moving white)
    def move(self, row, col, new_row, new_col):
        piece = self.board[row][col]
        # move the piece in pieces
        piece.move(new_row, new_col)
        # set new location to current piece
        self.board[new_row][new_col] = piece
        # set old position to free
        self.board[row][col] = 0

        # make it king if at end
        if self.player == 1 and new_row == self.rows - 1:
            piece.make_king()
        elif self.player == 2 and new_row == 0:
            piece.make_king()

        # record the move
        self.moves.append([(row, col), (new_row, new_col)])

        # change turns
        self.change_turn()

    # change turn of play, should be called from move
    def change_turn(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    # return if speicied position is valid
    # no longer need i think
    def valid_position(self, row, col):
        return (row >= 0 and row <= self.rows) and (col >= 0 and col <= self.cols)

    # check who's turn it is to play
    def whose_turn(self):
        return self.player

    # check to see if there is a winner
    def has_winner(self):
        return len(self.player2Pieces) == 0 or len(self.player2Pieces) == 0

    # if there is no more pieces left return who won
    def get_winner(self):
        if len(self.player2Pieces) == 0:
            return "Player 1 is Winner"
        elif len(self.player2Pieces) == 0:
            return "Player 2 is Winner"

    # itterate over all pieces of player that is not captured
    # find moves it can make and save it a list
    # return list
    def get_all_valid_moves(self):
        all_moves = []
        if self.player == 1:
            for piece in self.player1Pieces:
                if not piece.captured:
                    all_moves.extend(self.get_valid_moves(piece.row, piece.col, piece.color))
        else:
            for piece in self.player2Pieces:
                if not piece.captured:
                    all_moves.extend(self.get_valid_moves(piece.row, piece.col, piece.color))
        return all_moves

    # given a piece find position it can move to
    # find places it can move to - an right
    # returns new col and row, if it's a capturing move,
    # for each piece, call the lookForMove function for times with 4 directions
    # if capture_move returns not null, use the lookForMove function again

    def get_valid_moves(self, row, col, color):
        piece = self.board[row][col]
        if piece != 0:
            moves = []

            new_positions = []
            captured = True
            first_move = True
            while captured:
                if self.player == 1 or piece.king:
                    next_move = self._lookForMove(row, col, color, BOTTOMLEFT)  # player 1 move bottom left

                    if not next_move[1]:
                        if first_move:
                            moves.append(next_move)
                            first_move = False
                        else:
                            next_move = []
                        captured = False

                    self._lookForMove(row, col, color, BOTTOMRIGHT)  # player 1 move bottom right

                if self.player == 2 or piece.king:
                    self._lookForMove(row, col, color, TOPLEFT)  # player 2 move top left
                    self._lookForMove(row, col, color, TOPRIGHT)  # player 2 move top right


            if moves != []:
                return [([row, col], moves)]
        return []




    # seraches down left side of the board from given location
    # direction is where the piece will be moving towards
    # when it encounters a piece, not its own color,
    #          check if it can to a empty spot after captring
    #   (need to implement recursive capturing)
    # -----in progress capture
    # after getting back where it can move, call get_valid_moves to recurse
    # returns an array of two arrays, the next valid place to move to and the piece that's being captured
    # if there is no piece being captured, the second array is empty

    def _lookForMove(self, given_row, given_col, color, direction, needEmpty=False):
        new_places = []
        # check the left side it can move to
        if direction == BOTTOMLEFT and given_row + 1 < self.rows and given_col - 1 >= 0:
            new_places.append((given_row + 1, given_col - 1))  # bottom left
        elif direction == BOTTOMRIGHT and given_row + 1 < self.rows and given_col + 1 < self.cols:
            new_places.append((given_row + 1, given_col + 1))  # bottom right
        elif direction == TOPLEFT and given_row - 1 >= 0 and given_col - 1 >= 0:
            new_places.append((given_row - 1, given_col - 1))  # top left
        elif direction == TOPRIGHT and given_row - 1 >= 0 and given_col + 1 < self.cols:
            new_places.append((given_row - 1, given_col + 1))  # top right

        # check if there is empty piece or enemy piece in the way
        valid_place = []
        capture_piece = []

        # if the current position (new position after moving the piece to bottom left) is empty
        #   return the this
        #   position as new position and empty capture_piece array
        for row, col in new_places:
            if self.board[row][col] == 0:
                valid_place.extend([row, col])
                next_move = [valid_place, capture_piece]

                return next_move
            #
            # if the current position (new position after moving piece to bottom left) is not empty
            #     check if there exists an enemy piece
            #         if yes: check the position over this enemy piece, if it's within board
            #             if yes: check if it's empty
            #                 if yes: return that location as valid_place and
            #                         return the enemy piece location as capture_piece
            #
            else:
                if not needEmpty and self.board[row][col].color != color:
                    if direction == TOPLEFT:
                        if row - 1 >= 0 and col - 1 >= 0:
                            if self.board[row - 1][col - 1] == 0:
                                capture_piece.extend([row, col])
                                valid_place.extend([row - 1, col - 1])
                            else:
                                next_move = [valid_place, capture_piece]

                                return next_move
                    elif direction == TOPRIGHT:
                        if row - 1 >= 0 and col + 1 < self.cols:
                            if self.board[row - 1][col + 1] == 0:
                                capture_piece.extend([row, col])
                                valid_place.extend([row - 1, col + 1])
                            else:
                                next_move = [valid_place, capture_piece]

                                return next_move
                    elif direction == BOTTOMRIGHT:
                        if row + 1 < self.rows and col + 1 < self.cols:
                            if self.board[row + 1][col + 1] == 0:
                                capture_piece.extend([row, col])
                                valid_place.extend([row + 1, col + 1])
                            else:
                                next_move = [valid_place, capture_piece]

                                return next_move
                    elif direction == BOTTOMLEFT:
                        if row + 1 < self.rows and col - 1 >= 0:
                            if self.board[row + 1][col - 1] == 0:
                                capture_piece.extend([row, col])
                                valid_place.extend([row + 1, col - 1])
                            else:
                                next_move = [valid_place, capture_piece]

                                return next_move

        next_move = [valid_place, capture_piece]

        return next_move


    # given a move (current posititon, list of pieces with moves, index of piece, index of move)
    # will make the move, capture any piece in the way
    # given example:
    #    cur       new   |   cur      new      new   |    cur     new
    # [([1, 2], [(2, 1)]), ([3, 2], [(5, 0), (4, 3)]), ([1, 2], [(2, 1)])]
    def make_move(self, valid_moves, index_piece, index_move):
        # check if it has a piece location and move location
        move = valid_moves[index_piece]
        if len(move) != 2:
            return

        # get current piece location and move location
        row, col = move[0]
        new_row, new_col = move[1][index_move]

        print("Moving", self.playerColorShort[self.player], "From", (row, col), "to", (new_row, new_col))
        # move the piece
        self.move(row, col, new_row, new_col)

        # condition check to see if there is piece in the way we have to capture
        if abs(row - new_row) > 1 or abs(col - new_col) > 1:
            mid_row = (new_row + row) // 2
            mid_col = (new_col + col) // 2
            print("!!! Capturing", (mid_row, mid_col))
            remove_piece = self.board[mid_row][mid_col]
            remove_piece.capture()
            self.board[mid_row][mid_col] = 0


def main():
    board = Board()
    board.create_board()
    board.print_board()

    # red
    print("Player:", board.whose_turn())
    x = board.get_all_valid_moves()
    print(x)
    board.make_move(x, 0, 0)
    board.print_board()
    print()

    # white
    print("Player:", board.whose_turn())
    x = board.get_all_valid_moves()
    print(x)
    board.make_move(x, 0, 1)
    board.print_board()

    # red
    print("Player:", board.whose_turn())
    x = board.get_all_valid_moves()
    print(x)
    board.make_move(x, 2, 1)
    board.print_board()
    print()

    # white
    print("Player:", board.whose_turn())
    x = board.get_all_valid_moves()
    print(x)

    board.make_move(x, 2, 0)
    board.print_board()


main()