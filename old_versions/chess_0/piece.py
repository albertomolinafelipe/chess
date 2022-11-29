import pygame as pg
import os

b_pawn = pg.image.load(os.path.join("img", "b_pawn.png"))
b_bishop = pg.image.load(os.path.join("img", "b_bishop.png"))
b_knight = pg.image.load(os.path.join("img", "b_knight.png"))
b_rook = pg.image.load(os.path.join("img", "b_rook.png"))
b_queen = pg.image.load(os.path.join("img", "b_queen.png"))
b_king = pg.image.load(os.path.join("img", "b_king.png"))

w_pawn = pg.image.load(os.path.join("img", "w_pawn.png"))
w_bishop = pg.image.load(os.path.join("img", "w_bishop.png"))
w_knight = pg.image.load(os.path.join("img", "w_knight.png"))
w_rook = pg.image.load(os.path.join("img", "w_rook.png"))
w_queen = pg.image.load(os.path.join("img", "w_queen.png"))
w_king = pg.image.load(os.path.join("img", "w_king.png"))


class Piece:
    def __init__(self, color, row, col, board):
        
        self.color = color
        self.row = row
        self.col = col
        self.selected = False
        self.moves = []
        self.board = board
        self.moved = False
        self.castle = 0
        self.pawn = False

    def move(self, nrow, ncol):

        if self.castle == 1:
            self.board[self.row][7].move(self.row, 5)
        elif self.castle == 2:
            self.board[self.row][0].move(self.row, 3)
        self.castle = 0

        self.board[self.row][self.col] = None
        self.row = nrow
        self.col = ncol
        self.board[self.row][self.col] = self

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
        
class Pawn(Piece):
    def __init__(self, color, row, col, board):
        super().__init__(color, row, col, board)
        self.pawn = True
        if color == 'b':
            self.img = b_pawn
        else:
            self.img = w_pawn
    
    def updateMoves(self):
        ret = []

        if self.color == 'w':
            tmp0 = - 1
        else:
            tmp0 = 1

        # 1 foward 
        if 0 <= self.row + 1 * tmp0 < 8:
            if self.board[self.row + 1 * tmp0][self.col] is None:
                ret.append([self.row + 1 * tmp0, self.col])
        # First 2 foward
                if not self.moved:
                    if 0 <= self.row + 2 * tmp0 < 8:
                        if self.board[self.row + 2 * tmp0][self.col] is None:
                            ret.append([self.row + 2 * tmp0, self.col])
        # Taking diagonally
        tmp1 = 1
        for i in range(2):
            if 0 <= self.row + 1 * tmp0 < 8 and 0 <= self.col + tmp1 < 8:
                if self.board[self.row + 1 * tmp0][self.col + tmp1] is not None and self.board[self.row + 1 * tmp0][self.col + tmp1].color != self.color:
                    ret.append([self.row + 1 * tmp0, self.col + tmp1])
            tmp1 *= -1

        self.moves = ret

class Bishop(Piece):
    def __init__(self, color, row, col, board):
        super().__init__(color, row, col, board)
        if color == 'b':
            self.img = b_bishop
        else:
            self.img = w_bishop
    
    def updateMoves(self):
        ret = []
        
        # north east
        x = self.col + 1
        y = self.row - 1
        while 0 <= y < self.row and self.col < x <= 7:
            if self.board[y][x] is None:
                ret.append([y, x])
            else:
                if self.board[y][x].color != self.color:
                    ret.append([y, x])
                break
            x += 1
            y -= 1

        # south east
        x = self.col + 1
        y = self.row + 1
        while self.row < y <= 7 and self.col < x <= 7:
            if self.board[y][x] is None:
                ret.append([y, x])
            else:
                if self.board[y][x].color != self.color:
                    ret.append([y, x])
                break
            x += 1
            y += 1

        # south west
        x = self.col - 1
        y = self.row + 1
        while 0 <= x < self.col and self.row < y <= 7:
            if self.board[y][x] is None:
                ret.append([y, x])
            else:
                if self.board[y][x].color != self.color:
                    ret.append([y, x])
                break
            x -= 1
            y += 1

        # north west
        x = self.col - 1
        y = self.row - 1
        while 0 <= y < self.row and 0 <= x < self.col:
            if self.board[y][x] is None:
                ret.append([y, x])
            else:
                if self.board[y][x].color != self.color:
                    ret.append([y, x])
                break
            x -= 1
            y -= 1
        self.moves = ret

class Knight(Piece):
    def __init__(self, color, row, col, board):
        super().__init__(color, row, col, board)
        if color == 'b':
            self.img = b_knight
        else:
            self.img = w_knight
    
    def updateMoves(self):
        ret = []
        tmp0 = 1
        tmp1 = 1

        # north and south
        for x in range(2):
            if 0 <= self.row + 2 * tmp1 < 8:
                for i in range(2):
                    if 0 <= self.col + 1 * tmp0 < 8:
                        if self.board[self.row + 2 * tmp1][self.col + 1 * tmp0] is None or \
                            self.board[self.row + 2 * tmp1][self.col + 1 * tmp0].color != self.color:
                            ret.append([self.row + 2 * tmp1, self.col + 1 * tmp0])
                    tmp0 *= -1
            tmp1 *= -1

        # east and west
        for x in range(2):
            if 0 <= self.col + 2 * tmp1 < 8:
                for i in range(2):
                    if 0 <= self.row + 1 * tmp0 < 8:
                        if self.board[self.row + 1 * tmp0][self.col + 2 * tmp1] is None or \
                            self.board[self.row + 1 * tmp0][self.col + 2 * tmp1].color != self.color:
                            ret.append([self.row + 1 * tmp0, self.col + 2 * tmp1])
                    tmp0 *= -1
            tmp1 *= -1

        self.moves = ret

class Rook(Piece):
    def __init__(self, color, row, col, board):
        super().__init__(color, row, col, board)
        if color == 'b':
            self.img = b_rook
        else:
            self.img = w_rook
    
    def updateMoves(self):
        ret = []

        # north
        y = self.row - 1
        while 0 <= y < self.row:
            if self.board[y][self.col] is None:
                ret.append([y, self.col])
            else:
                if self.board[y][self.col].color != self.color:
                    ret.append([y, self.col])
                break
            y -= 1

        # south
        y = self.row + 1
        while self.row < y <= 7:
            if self.board[y][self.col] is None:
                ret.append([y, self.col])
            else:
                if self.board[y][self.col].color != self.color:
                    ret.append([y, self.col])
                break
            y += 1

        # east
        x = self.col + 1
        while self.col < x <= 7:
            if self.board[self.row][x] is None:
                ret.append([self.row, x])
            else:
                if self.board[self.row][x].color != self.color:
                    ret.append([self.row, x])
                break
            x += 1

        # west
        x = self.col - 1
        while 0 <= x < self.col:
            if self.board[self.row][x] is None:
                ret.append([self.row, x])
            else:
                if self.board[self.row][x].color != self.color:
                    ret.append([self.row, x])
                break
            x -= 1

        self.moves = ret

class King(Piece):
    def __init__(self, color, row, col, board):
        super().__init__(color, row, col, board)
        self.king = True
        if color == 'b':
            self.img = b_king
        else:
            self.img = w_king

    def updateMoves(self):
        ret = []
        for i in range(-1,2):
            for j in range(-1,2):
                x = self.col + i
                y = self.row + j
                if 0 <= x < 8 and 0 <= y < 8 and not (i == 0 and j == 0):
                    if self.board[y][x] is None:
                        ret.append([y, x])
                    else:
                        if self.board[y][x].color != self.color:
                            ret.append([y, x])
        
        # Short castle
        if not self.moved:
            if self.board[self.row][6] is None and self.board[self.row][5] is None and\
                self.board[self.row][7] is not None and not self.board[self.row][7].moved:
                ret.append([self.row, 6])
                self.castle = 1
        # Long castle
            if self.board[self.row][3] is None and self.board[self.row][2] is None and\
                self.board[self.row][1] is None and not self.board[self.row][0].moved:
                ret.append([self.row, 2])
                self.castle = 2

        self.moves = ret

class Queen(Piece):
    def __init__(self, color, row, col, board):
        super().__init__(color, row, col, board)
        if color == 'b':
            self.img = b_queen
        else:
            self.img = w_queen

    def updateMoves(self):
        ret = []

        # north
        y = self.row - 1
        while 0 <= y < self.row:
            if self.board[y][self.col] is None:
                ret.append([y, self.col])
            else:
                if self.board[y][self.col].color != self.color:
                    ret.append([y, self.col])
                break
            y -= 1

        # south
        y = self.row + 1
        while self.row < y <= 7:
            if self.board[y][self.col] is None:
                ret.append([y, self.col])
            else:
                if self.board[y][self.col].color != self.color:
                    ret.append([y, self.col])
                break
            y += 1

        # east
        x = self.col + 1
        while self.col < x <= 7:
            if self.board[self.row][x] is None:
                ret.append([self.row, x])
            else:
                if self.board[self.row][x].color != self.color:
                    ret.append([self.row, x])
                break
            x += 1

        # west
        x = self.col - 1
        while 0 <= x < self.col:
            if self.board[self.row][x] is None:
                ret.append([self.row, x])
            else:
                if self.board[self.row][x].color != self.color:
                    ret.append([self.row, x])
                break
            x -= 1

        # north east
        x = self.col + 1
        y = self.row - 1
        while 0 <= y < self.row and self.col < x <= 7:
            if self.board[y][x] is None:
                ret.append([y, x])
            else:
                if self.board[y][x].color != self.color:
                    ret.append([y, x])
                break
            x += 1
            y -= 1

        # south east
        x = self.col + 1
        y = self.row + 1
        while self.row < y <= 7 and self.col < x <= 7:
            if self.board[y][x] is None:
                ret.append([y, x])
            else:
                if self.board[y][x].color != self.color:
                    ret.append([y, x])
                break
            x += 1
            y += 1

        # south west
        x = self.col - 1
        y = self.row + 1
        while 0 <= x < self.col and self.row < y <= 7:
            if self.board[y][x] is None:
                ret.append([y, x])
            else:
                if self.board[y][x].color != self.color:
                    ret.append([y, x])
                break
            x -= 1
            y += 1

        # north west
        x = self.col - 1
        y = self.row - 1
        while 0 <= y < self.row and 0 <= x < self.col:
            if self.board[y][x] is None:
                ret.append([y, x])
            else:
                if self.board[y][x].color != self.color:
                    ret.append([y, x])
                break
            x -= 1
            y -= 1

        self.moves = ret