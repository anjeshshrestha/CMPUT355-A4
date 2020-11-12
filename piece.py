class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.captured = False
    
    def move(self, row, col):
        self.row = row
        self.col = col

    def get_column(self):
        return self.col

    def get_row(self):
        return self.row

    def get_color(self):
        return self.color

    def can_move(self):
        return not self.captured

    def capture(self):
        self.captured = True

    def make_king(self):
        self.king = True