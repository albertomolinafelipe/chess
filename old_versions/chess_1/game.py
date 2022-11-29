import numpy as np
import pygame as pg
from piece import Pawn, Bishop, Rook, Knight, King, Queen
from ai import AI
import time

""" 
- lets the player choose the color
- At each turn:
    - Get all possible moves
    - look for check
        - Check without having moved a piece is the easy one
        - Check that a move doesnt leave the king in check
    - let the player choose a move from the list
        - At any given time, the game or computer aks each piece for the moves they can do given a board
        - the player CHOOSES
        - the game MOVES
    
"""

palette = {
    'dark_tile' : (148, 132, 114),
    'light_tile' : (255, 255, 240),

    'dark_move' : (99, 153, 235),
    'ligth_move' : (133, 193, 233),
    'dark_selected' : (249, 176, 94),
    'ligth_selected' : (249, 195, 135),
    'piece_selected' : (99, 153, 235),

    'dark_ai_move' : (231, 76, 60),
    'light_ai_move' : (236, 112, 99),

    'black': (0, 0, 0),
    'white' : (255, 255, 255),
    'grey' : (120, 120, 120)
}


class Game:

    def __init__(self, size=480):

        self.user_color = None
        self.board = []
        self.turn = -1
        self.not_moves = []
        self.piece_selected = None
        self.winner = None
        self.ai = AI()
        self.user_moves = [] # just for display
        self.user_move = [] # just for display
        self.ai_move = [] # just for display
        self.kings = [] # just for display

        # Needed for pygame
        self.running = True
        self.size = size
        pg.init()
        self.font = pg.font.SysFont('chalkdusterttf.ttf', 40) 
        self.screen = pg.display.set_mode((size, size)) 

    def boardInit(self):
        """ Place all the pieces accordingly """
        matrix = np.full([8,8], None)

        if self.user_color == 1:
            top = -1
            king_col = 3
            queen_col = 4
        else:
            top = 1
            king_col = 4
            queen_col = 3
        bottom = self.user_color

        for i in range(8):
            # pawns
            matrix[1][i] = Pawn(top, 1, i)
            matrix[6][i] = Pawn(bottom, 6, i)
        # rooks
        matrix[0][0] = Rook(top, 0, 0)
        matrix[0][7] = Rook(top, 0, 7)
        matrix[7][0] = Rook(bottom, 7, 0)
        matrix[7][7] = Rook(bottom, 7, 7)
        # knights
        matrix[0][1] = Knight(top, 0, 1)
        matrix[0][6] = Knight(top, 0, 6)
        matrix[7][1] = Knight(bottom, 7, 1)
        matrix[7][6] = Knight(bottom, 7, 6)
        # bishop
        matrix[0][2] = Bishop(top, 0, 2)
        matrix[0][5] = Bishop(top, 0, 5)
        matrix[7][2] = Bishop(bottom, 7, 2)
        matrix[7][5] = Bishop(bottom, 7, 5)
        # queen
        matrix[0][queen_col] = Queen(top, 0, queen_col)
        matrix[7][queen_col] = Queen(bottom, 7, queen_col)
        #kings
        matrix[0][king_col] = King(top, 0, king_col)
        matrix[7][king_col] = King(bottom, 7, king_col) 

        if top == -1: # white first, easier later
            self.kings = [matrix[0][king_col], matrix[7][king_col]]
        else:
            self.kings = [matrix[7][king_col], matrix[0][king_col]]

        self.board = matrix
        
    def getMoves(self, board, color):
        """ Gets all the moves give a board and color, these are given as
        attributes because its need to look into the effects of unmade moves"""
        moves = []
        for row in self.board:
            for piece in row:
                if piece is not None and piece.color == color:
                    pieces_move = piece.updateMoves(board)
                    for move in pieces_move:
                        if move not in self.not_moves:
                            moves.append(move)
        return moves

    def lookForCheck(self, board):
        """ Looks for check given a board"""
        check = False

        moves = self.getMoves(board, self.turn * -1)
        for i, row in enumerate(board):
            for j, piece in enumerate(row):
                if piece is not None and piece.special == 2 and piece.color == self.turn: # king
                    king_pos = [i, j]
        
        for tmp in moves:
            for move in tmp:
                if move[1] == king_pos:
                    check = True
        return check

    def startTurn(self):

        self.not_moves = []
        checkmate = True
        all_moves = self.getMoves(self.board, self.turn)
        for move in all_moves:
            # hacer copia de la tabla
            untouched = self.board.copy()
            if not self.lookForCheck(self.movePiece(self.board, move, real=False)):
                checkmate = False
            else:
                self.not_moves.append(move)
            self.board = untouched.copy()

        if checkmate:
            self.winner = self.turn * -1
        
        # AI !!
        if self.user_color != self.turn and self.winner is None:
            self.ai_move = self.ai.makeMove(self.getMoves(self.board, self.turn))
            self.movePiece(self.board, self.ai_move)
            self.turn *= -1
            self.piece_selected = None
            self.startTurn()

    def movePiece(self, board, move_, real=True):
        for move in move_:
            piece = board[move[0][0]][move[0][1]]
            if real:
                piece.moved = True
                piece.row = move[1][0]
                piece.col = move[1][1]
                if piece.special == 1: # Pawn to queen
                    if move[1][0] == 0 or move[1][0] == 7:
                        del piece
                        piece = Queen(self.turn, move[1][0], move[1][1])
            board[move[0][0]][move[0][1]] = None
            board[move[1][0]][move[1][1]] = piece
        return board

    def click(self, row, col):
        """ Manages where the user clicks and what it means"""
        if self.user_color is None:
            # Row will be px
            if 0 <= row < 3 * self.size / 8:
                self.user_color = 1
            elif 3 * self.size / 8 <= row < 5 * self.size / 8:
                self.user_color = np.random.choice([1, -1])
            else:
                self.user_color = -1
            self.boardInit()
            self.startTurn()

        # Select piece USER
        elif self.board[row][col] is not None and self.board[row][col].color == self.user_color:
            self.piece_selected = self.board[row][col]
            all_moves = self.piece_selected.updateMoves(self.board)
            good_ones = []
            for move in all_moves:
                if move not in self.not_moves:
                    good_ones.append(move)
            self.user_moves = good_ones

        # Move USER
        elif self.piece_selected is not None:
            for move in self.user_moves:
                if row == move[0][1][0] and col == move[0][1][1]:
                    self.user_move = move
                    self.movePiece(self.board, move)
                    self.turn *= -1
                    self.piece_selected = None
                    self.startTurn()

    def run(self):
        while self.running:
            self.draw()
            if self.user_color is None:
                pg.display.set_caption("CHOOSE A COLOR")
            else:
                if self.turn == -1:
                    pg.display.set_caption("CHESS_1: white's turn")
                else:
                    pg.display.set_caption("CHESS_1: black's turn")                
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    # Color selection
                    if self.user_color is None:
                        self.click(event.pos[0], event.pos[1])
                    else:
                        col = int(event.pos[0] // (self.size/8))
                        row = int(event.pos[1] // (self.size/8))
                        self.click(row, col)
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()

    def draw(self):
        """ - Ask for color
            - Blank board
            - Highlighted positions
            - Pieces
            - Lines """
        
        if self.user_color is None:
            left_rect = (0, 0, 3*self.size/8, self.size)
            mid_rect = (3*self.size/8, 0, 2*self.size/8, self.size)
            right_rect = (5*self.size/8, 0, 3*self.size/8, self.size)
            # Inside
            pg.draw.rect(self.screen, palette['black'], left_rect)
            pg.draw.rect(self.screen, palette['grey'], mid_rect)
            pg.draw.rect(self.screen, palette['white'], right_rect)

            img0 = self.font.render('B', True, palette['white']) 
            img1 = self.font.render('?', True, palette['dark_ai_move'])
            img2 = self.font.render('W', True, palette['black'])

            self.screen.blit(img0, (int(3*self.size/16 - 10), int(self.size/2)))
            self.screen.blit(img1, (int(self.size/2 - 10), int(self.size/2)))
            self.screen.blit(img2, (int(13*self.size/16- 10), int(self.size/2)))

        elif self.winner is not None:
            if self.winner == -1: # white
                pg.draw.rect(self.screen, palette['white'], (0, 0, self.size, self.size))
                res = self.font.render('WHITE WINS', True, palette['black']) 
                self.screen.blit(res, (int(0.25*self.size + 35), int(0.25*self.size)))
                self.screen.blit(self.kings[1].img, (self.size/2-25,self.size/2-60))
            if self.winner == 1:
                pg.draw.rect(self.screen, palette['black'], (0, 0, self.size, self.size))
                res = self.font.render('BLACK WINS', True, palette['white']) 
                self.screen.blit(res, (int(0.25*self.size + 35), int(0.25*self.size)))
                self.screen.blit(self.kings[0].img, (self.size/2-25,self.size/2-60))
            else:
                pass

        else:
            # blank board
            for row in range(8):
                for col in range(8):
                    self.drawTiles(row, col, palette['light_tile'], palette['dark_tile'])

            # piece selected
            if self.piece_selected is not None:
                self.drawTiles(self.piece_selected.row, self.piece_selected.col, palette['piece_selected'], palette['piece_selected'])
        
            # AI LAST moves
            if len(self.ai_move) > 0:
                orow = self.ai_move[0][0][0]
                ocol = self.ai_move[0][0][1]
                drow = self.ai_move[0][1][0]
                dcol = self.ai_move[0][1][1]
                self.drawTiles(orow, ocol, palette['light_ai_move'], palette['dark_ai_move'])
                self.drawTiles(drow, dcol, palette['light_ai_move'], palette['dark_ai_move'])
            
            # User LAST move
            if len(self.user_move) > 0:
                orow = self.user_move[0][0][0]
                ocol = self.user_move[0][0][1]
                drow = self.user_move[0][1][0]
                dcol = self.user_move[0][1][1]
                self.drawTiles(orow, ocol, palette['ligth_move'], palette['dark_move'])
                self.drawTiles(drow, dcol, palette['ligth_move'], palette['dark_move'])
            
            # moves 
            if self.piece_selected is not None:
                for move in self.user_moves:
                    row = move[0][1][0]
                    col = move[0][1][1]
                    self.drawTiles(row, col, palette['ligth_selected'], palette['dark_selected'])


            # Pieces
            for j, row in enumerate(self.board):
                for i, piece in enumerate(row):
                    if piece is not None:
                        self.screen.blit(piece.img, (piece.col * self.size/8, piece.row * self.size/8))

            # lines
            for row in range(8):
                for col in range(8):
                    rect = (row * self.size/8, col * self.size/8, self.size/8, self.size/8)
                    pg.draw.rect(self.screen, palette['black'], rect, 1)

        pg.display.flip()
        pass

    def drawTiles(self, row, col, light, dark):
        rect = (col * self.size/8, row * self.size/8, self.size/8, self.size/8)
        if (col + row) % 2:
            pg.draw.rect(self.screen, dark, rect)
        else:
            pg.draw.rect(self.screen, light, rect)

def main():
    Game().run()

if __name__ == '__main__':
    main()