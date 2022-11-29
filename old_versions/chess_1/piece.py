import pygame as pg
import os
import numpy as np

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
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        # For pawn and king
        self.special = 0
        self.moved = False
    
    def checkPos(self, row, col, board):
        if 0 <= row < 8 and 0 <= col < 8:
            if board[row][col] is None:
                return 0 # empty
            if board[row][col].color != self.color:
                return 1 # foe
            else:
                return 2 # friend
        else:
            return -1 # mistake

class Pawn(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.dir = None
        self.special = 1
        if color == 1:
            self.img = b_pawn
        else:
            self.img = w_pawn
    
    def updateMoves(self, board):
        ret = []
        pos = [self.row, self.col]
        # Get direction
        if self.dir is None:
            if self.row < 4:
                self.dir = 1 # down
            else:
                self.dir = -1 # up
        # 1 foward
        if self.checkPos(self.row + 1 * self.dir, self.col, board) == 0:
            ret.append([[pos, [self.row + 1 * self.dir, self.col]]])
        # First 2 foward
            if self.dir > 0:
                starting_tile = 1
            else:
                starting_tile = 6
            if self.row == starting_tile and self.checkPos(self.row + 2*self.dir, self.col, board) == 0:
                ret.append([[pos, [self.row + 2*self.dir, self.col]]])
        # Taking diagonally
        for i in range(-1, 2, 2):
            if self.checkPos(self.row + 1*self.dir, self.col + i, board) == 1:
                ret.append([[pos, [self.row + 1*self.dir, self.col + i]]])
        return ret

class Bishop(Piece):
    def __init__(self, color, row, col, ):
        super().__init__(color, row, col, )
        if color == 1:
            self.img = b_bishop
        else:
            self.img = w_bishop
    
    def updateMoves(self, board):
        ret = []
        pos = [self.row, self.col]
        
        # north east
        row = self.row - 1
        col = self.col + 1
        while 0 <= row < self.row and self.col < col <= 7:
            tmp = self.checkPos(row, col, board)
            if 0 <= tmp <= 1:
                ret.append([[pos, [row, col]]])
            if 1 <= tmp <= 2:
                break
            col += 1
            row -= 1

        # south east
        col = self.col + 1
        row = self.row + 1
        while self.row < row <= 7 and self.col < col <= 7:
            tmp = self.checkPos(row, col, board)
            if 0 <= tmp <= 1:
                ret.append([[pos, [row, col]]])
            if 1 <= tmp <= 2:
                break
            col += 1
            row += 1

        # south west
        col = self.col - 1
        row = self.row + 1
        while 0 <= col < self.col and self.row < row <= 7:
            tmp = self.checkPos(row, col, board)
            if 0 <= tmp <= 1:
                ret.append([[pos, [row, col]]])
            if 1 <= tmp <= 2:
                break
            col -= 1
            row += 1

        # north west
        col = self.col - 1
        row = self.row - 1
        while 0 <= row < self.row and 0 <= col < self.col:
            tmp = self.checkPos(row, col, board)
            if 0 <= tmp <= 1:
                ret.append([[pos, [row, col]]])
            if 1 <= tmp <= 2:
                break
            col -= 1
            row -= 1

        return ret

class Knight(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col, )
        if color == 1:
            self.img = b_knight
        else:
            self.img = w_knight
    
    def updateMoves(self, board):
        ret = []
        pos =  [self.row, self.col]
        # bottom 2
        if 0 <= self.checkPos(self.row + 2, self.col + 1, board) <= 1:
            ret.append([[pos, [self.row + 2, self.col + 1]]])
        if 0 <= self.checkPos(self.row + 2, self.col - 1, board) <= 1:
            ret.append([[pos, [self.row + 2, self.col - 1]]])
        # top 2
        if 0 <= self.checkPos(self.row - 2, self.col + 1, board) <= 1:
            ret.append([[pos, [self.row - 2, self.col + 1]]])
        if 0 <= self.checkPos(self.row - 2, self.col - 1, board) <= 1:
            ret.append([[pos, [self.row - 2, self.col - 1]]])
        # right 2
        if 0 <= self.checkPos(self.row + 1, self.col + 2, board) <= 1:
            ret.append([[pos, [self.row + 1, self.col + 2]]])
        if 0 <= self.checkPos(self.row - 1, self.col + 2, board) <= 1:
            ret.append([[pos, [self.row - 1, self.col + 2]]])
        # left 2
        if 0 <= self.checkPos(self.row + 1, self.col - 2, board) <= 1:
            ret.append([[pos, [self.row + 1, self.col - 2]]])
        if 0 <= self.checkPos(self.row - 1, self.col - 2, board) <= 1:
            ret.append([[pos, [self.row - 1, self.col - 2]]])

        return ret

class Rook(Piece):
    def __init__(self, color, row, col, ):
        super().__init__(color, row, col, )
        if color == 1:
            self.img = b_rook
        else:
            self.img = w_rook
    
    def updateMoves(self, board):
        ret = []
        pos = [self.row, self.col]

        # north
        row = self.row - 1
        while 0 <= row < self.row:
            tmp = self.checkPos(row, self.col, board)
            if 0 <= tmp <= 1:
                ret.append([[pos, [row, self.col]]])
            if 1 <= tmp <= 2:
                break
            row -= 1

        # south
        row = self.row + 1
        while self.row < row <= 7:
            tmp = self.checkPos(row, self.col, board)
            if 0 <= tmp <= 1:
                ret.append([[pos, [row, self.col]]])
            if 1 <= tmp <= 2:
                break
            row += 1

        # east
        col = self.col + 1
        while self.col < col <= 7:
            tmp = self.checkPos(self.row, col, board)
            if 0 <= tmp <= 1:
                ret.append([[pos, [self.row, col]]])
            if 1 <= tmp <= 2:
                break
            col += 1

        # west
        col = self.col - 1
        while 0 <= col < self.col:
            tmp = self.checkPos(self.row, col, board)
            if 0 <= tmp <= 1:
                ret.append([[pos, [self.row, col]]])
            if 1 <= tmp <= 2:
                break
            col -= 1

        self.moves = ret

        return ret

class King(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.special = 2
        if color == 1:
            self.img = b_king
        else:
            self.img = w_king

    def updateMoves(self, board):
        ret = []
        pos = [self.row, self.col]
        for i in range(-1,2):
            for j in range(-1,2):
                row = self.row + i
                col = self.col + j
                if not (i == 0 and j == 0):
                    if 0 <= self.checkPos(row, col, board) <= 1:
                        ret.append([[pos, [row, col]]])

        if not self.moved and self.col == 4:
            # white is at the bottom
            # short castle
            if board[self.row][5] is None and board[self.row][6] is None and\
                board[self.row][7] is not None and not board[self.row][7].moved:
                    ret.append([[pos, [self.row, self.col+2]],
                                [[self.row, 7], [self.row, self.col+1]]])
            # long castle
            if board[self.row][3] is None and board[self.row][2] is None and\
                board[self.row][1] is None and board[self.row][0] is not None and\
                not board[self.row][0].moved:
                ret.append([[pos, [self.row, self.col-2]],
                            [[self.row, 0], [self.row, self.col-1]]])

        if not self.moved and self.col == 3:
            # black is at the bottom
            # short castle
            if board[self.row][2] is None and board[self.row][1] is None and\
                board[self.row][0] is not None and not board[self.row][0].moved:
                    ret.append([[pos, [self.row, self.col-2]],
                                [[self.row, 0], [self.row, self.col-1]]])
            # long castle
            if board[self.row][4] is None and board[self.row][5] is None and\
                board[self.row][6] is None and board[self.row][7] is not None and\
                not board[self.row][7].moved:
                ret.append([[pos, [self.row, self.col+2]],
                            [[self.row, 7], [self.row, self.col+1]]])
        return ret

class Queen(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        if color == 1:
            self.img = b_queen
        else:
            self.img = w_queen

    def updateMoves(self, board):
        ret = []
        pos = [self.row, self.col]

        # north
        row = self.row - 1
        while 0 <= row < self.row:
            tmp = self.checkPos(row, self.col, board)
            if 0 <= tmp <= 1:
                ret.append([[pos, [row, self.col]]])
            if 1 <= tmp <= 2:
                break
            row -= 1

        # south
        row = self.row + 1
        while self.row < row <= 7:
            tmp = self.checkPos(row, self.col, board)
            if 0 <= tmp <= 1:
                ret.append([[pos, [row, self.col]]])
            if 1 <= tmp <= 2:
                break
            row += 1

        # east
        col = self.col + 1
        while self.col < col <= 7:
            tmp = self.checkPos(self.row, col, board)
            if 0 <= tmp <= 1:
                ret.append([[pos, [self.row, col]]])
            if 1 <= tmp <= 2:
                break
            col += 1

        # west
        col = self.col - 1
        while 0 <= col < self.col:
            tmp = self.checkPos(self.row, col, board)
            if 0 <= tmp <= 1:
                ret.append([[pos, [self.row, col]]])
            if 1 <= tmp <= 2:
                break
            col -= 1

        self.moves = ret

                # north east
        row = self.row - 1
        col = self.col + 1
        while 0 <= row < self.row and self.col < col <= 7:
            tmp = self.checkPos(row, col, board)
            if 0 <= tmp <= 1:
                ret.append([[pos, [row, col]]])
            if 1 <= tmp <= 2:
                break
            col += 1
            row -= 1

        # south east
        col = self.col + 1
        row = self.row + 1
        while self.row < row <= 7 and self.col < col <= 7:
            tmp = self.checkPos(row, col, board)
            if 0 <= tmp <= 1:
                ret.append([[pos, [row, col]]])
            if 1 <= tmp <= 2:
                break
            col += 1
            row += 1

        # south west
        col = self.col - 1
        row = self.row + 1
        while 0 <= col < self.col and self.row < row <= 7:
            tmp = self.checkPos(row, col, board)
            if 0 <= tmp <= 1:
                ret.append([[pos, [row, col]]])
            if 1 <= tmp <= 2:
                break
            col -= 1
            row += 1

        # north west
        col = self.col - 1
        row = self.row - 1
        while 0 <= row < self.row and 0 <= col < self.col:
            tmp = self.checkPos(row, col, board)
            if 0 <= tmp <= 1:
                ret.append([[pos, [row, col]]])
            if 1 <= tmp <= 2:
                break
            col -= 1
            row -= 1

        return ret