from cmath import pi
from ssl import OP_NO_COMPRESSION
import pygame as pg
import numpy as np
import os
import time

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

b_pawn_ai = pg.image.load(os.path.join("img", "b_pawn_ai.png"))
b_bishop_ai = pg.image.load(os.path.join("img", "b_bishop_ai.png"))
b_knight_ai = pg.image.load(os.path.join("img", "b_knight_ai.png"))
b_rook_ai = pg.image.load(os.path.join("img", "b_rook_ai.png"))
b_queen_ai = pg.image.load(os.path.join("img", "b_queen_ai.png"))
b_king_ai = pg.image.load(os.path.join("img", "b_king_ai.png"))

w_pawn_ai = pg.image.load(os.path.join("img", "w_pawn_ai.png"))
w_bishop_ai = pg.image.load(os.path.join("img", "w_bishop_ai.png"))
w_knight_ai = pg.image.load(os.path.join("img", "w_knight_ai.png"))
w_rook_ai = pg.image.load(os.path.join("img", "w_rook_ai.png"))
w_queen_ai = pg.image.load(os.path.join("img", "w_queen_ai.png"))
w_king_ai = pg.image.load(os.path.join("img", "w_king_ai.png"))

symbol_ai = pg.image.load(os.path.join("img", "symbol_ai.png"))
symbol_user = pg.image.load(os.path.join("img", "symbol_user.png"))

colors = {
    'black' : (0, 0, 0),
    'white' : (255, 255, 255),
    'grey' : (80, 80, 80),
    'red' : (252, 32, 2),
    'brown' : (128, 68, 43),
    'beige' : (246, 227, 197),

    # selected piece
    'selected_dark': (170, 45, 32),
    'selected_light' : (252, 76, 66),

    # top available moves
    'top_available_dark' : (213, 105, 14),
    'top_available_light' : (252, 158, 66),
    # bottom available moves
    'bottom_available_dark' : (94, 138, 60),
    'bottom_available_light' : (123, 178, 99)
    
}



class UI:
    def __init__(self, size, controller) -> None:

        self.white_ai = False
        self.black_ai = False
        # How to orient the board
        self.orientation = 0
        self.pregame_state = 0
        self.last_move = None

        self.size = size
        pg.init()
        self.font = pg.font.SysFont('couriernew.ttf', 40) 
        self.screen = pg.display.set_mode((size, size))

    def getPreGame(self):
        ai = 0
        while True:
            self.drawPreGame()
            if self.pregame_state == 0:
                pg.display.set_caption("Select Player Mode")
            if self.pregame_state == 1:
                pg.display.set_caption("Select P1 Color")

            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    px = event.pos[0]
                    # Color selection
                    if self.pregame_state == 0:
                        if self.size/3 <= px < 2*self.size/3:
                            ai = 1
                        elif 2*self.size/3 <= px <= self.size:
                            ai = 2
                            self.orientation = 0
                            self.white_ai = True
                            self.black_ai = True
                            return self.white_ai, self.black_ai
                        self.pregame_state += 1
                    elif self.pregame_state == 1:
                        if 0 <= px < self.size/3: # p1 black
                            self.orientation = 1
                        elif self.size/3 <= px < 2*self.size/3: # random
                            if np.random.rand() < 0.5:
                                self.orientation = 1
                            else:
                                self.orientation = 0
                        else: # p1 white
                            self.orientation = 0

                        if (self.orientation == 0 and ai == 1) or ai == 2:
                            self.black_ai = True
                        if (self.orientation == 1 and ai == 1) or ai == 2:
                            self.white_ai = True
                        return self.white_ai, self.black_ai
                if event.type == pg.QUIT:
                    pg.quit()
                    return -1, -1

    def drawPreGame(self):
        left_rect = (0, 0, self.size/3, self.size)
        mid_rect = (self.size/3, 0, self.size/3, self.size)
        right_rect = (2*self.size/3, 0, self.size/3, self.size)

        if self.pregame_state == 0:
            self.screen.fill(colors['grey'])
            pg.draw.rect(self.screen, colors['white'], left_rect, 1)
            pg.draw.rect(self.screen, colors['white'], mid_rect, 1)
            pg.draw.rect(self.screen, colors['white'], right_rect, 1)

            vs = self.font.render('vs.', True, colors['white'])

            self.screen.blit(symbol_user, (int(self.size/6 - 32), int(self.size/4 + 32)))
            self.screen.blit(vs, (int(self.size/6 - 15), int(self.size/2)))
            self.screen.blit(symbol_user, (int(self.size/6 - 32), int(3*self.size/4 - 70)))

            self.screen.blit(symbol_ai, (int(self.size/2 - 32), int(self.size/4 + 32)))
            self.screen.blit(vs, (int(self.size/2 - 15), int(self.size/2)))
            self.screen.blit(symbol_user, (int(self.size/2 - 32), int(3*self.size/4 - 70)))

            self.screen.blit(symbol_ai, (int(5*self.size/6 - 32), int(self.size/4 + 32)))
            self.screen.blit(vs, (int(5*self.size/6 - 15), int(self.size/2)))
            self.screen.blit(symbol_ai, (int(5*self.size/6 - 32), int(3*self.size/4 - 70)))
        else:
            pg.draw.rect(self.screen, colors['black'], left_rect)
            pg.draw.rect(self.screen, colors['grey'], mid_rect)
            pg.draw.rect(self.screen, colors['white'], right_rect)

            img0 = self.font.render('B', True, colors['white']) 
            img1 = self.font.render('?', True, colors['red'])
            img2 = self.font.render('W', True, colors['black'])

            self.screen.blit(img0, (int(self.size/6 - 10), int(self.size/2)))
            self.screen.blit(img1, (int(self.size/2 - 10), int(self.size/2)))
            self.screen.blit(img2, (int(5*self.size/6 - 10), int(self.size/2)))
        pg.display.flip()

    def getMove(self, all_moves, board, ai_move=None, end=False):
        turn = board[-2]
        losser = board[-1]
        piece_selected = None
        piece_moves = []
        selected_pos = []
        if ai_move is not None:
            piece_moves =[ai_move]
        
        board = board[:-5]
        board.shape = (8,8)

        start = time.time()

        while True:
            if ai_move is not None and time.time() > start + .1:
                return 0
                break
            if not end:
                self.drawMoveSelection(board, selected_pos, piece_moves, ai_move is not None)
                if turn == '1':
                    pg.display.set_caption("CHESS_2: BLACK MOVES")
                else:
                    pg.display.set_caption("CHESS_2: WHITE MOVES")
            else:
                self.drawMoveSelection(board, selected_pos, piece_moves, ai_move is not None)
                if losser == '1':
                    pg.display.set_caption("-- WHITE WINS --")
                elif losser == '0':
                    pg.display.set_caption("-- BLACK WINS --")
                else:
                    pg.display.set_caption('-- DRAW --')

            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    col = int(event.pos[0]//(self.size/8))
                    row = int(event.pos[1]//(self.size/8))

                    # Piece selection
                    if ai_move is None:
                        if not self.orientation:
                            if board[row][col] != '0' and board[row][col][-1] == turn:
                                piece_selected = board[row][col]
                                selected_pos = [row, col]
                                piece_moves = []
                                for move in all_moves:
                                    if str(row)+str(col) == move[:-2]:
                                        piece_moves.append(move)
                        else:
                            if board[7-row][7-col] != '0' and board[7-row][7-col][-1] == turn:
                                piece_selected = board[7-row][7-col]
                                selected_pos = [row, col]
                                piece_moves = []
                                for move in all_moves:
                                    if str(7-row)+str(7-col) == move[:-2]:
                                        piece_moves.append(move)
                        # Move selection
                        if piece_selected is not None:
                            for move in piece_moves:
                                if self.orientation:
                                    if str(7-row)+str(7-col) == move[-2:]:
                                        self.last_move = move
                                        return move
                                else:
                                    if str(row)+str(col) == move[-2:]:
                                        self.last_move = move
                                        return move

                if event.type == pg.QUIT:
                    pg.quit()
                    return -1

    def drawMoveSelection(self, board, selected, moves, ai_move):

        if self.orientation:
                board = np.rot90(board, k=2, axes=(1,0))

        for i, row in enumerate(board):
            for j, piece in enumerate(row):
                rect = (j * self.size/8, i * self.size/8, self.size/8, self.size/8)
                # Tiles
                if (i + j) % 2:
                    pg.draw.rect(self.screen, colors['brown'], rect)
                else:
                    pg.draw.rect(self.screen, colors['beige'], rect)
                
                # Selected tile
                if [i,j] == selected:
                    if (i + j) % 2:
                        pg.draw.rect(self.screen, colors['selected_dark'], rect)
                    else:
                        pg.draw.rect(self.screen, colors['selected_light'], rect)

        # Last move
        if self.last_move is not None:
            if self.orientation:
                i = 7 - int(self.last_move[-2])
                j = 7 - int(self.last_move[-1])
                x = 7 - int(self.last_move[-4])
                y = 7 - int(self.last_move[-3])
            else:
                i = int(self.last_move[-2])
                j = int(self.last_move[-1])
                x = int(self.last_move[-4])
                y = int(self.last_move[-3])
            if board[i][j][-1] == str(self.orientation):
                cl = [colors['bottom_available_dark'], colors['bottom_available_light']]
            else:
                cl = [colors['top_available_dark'], colors['top_available_light']]

            rect = (j * self.size/8, i * self.size/8, self.size/8, self.size/8)
            if (i + j) % 2:
                pg.draw.rect(self.screen, cl[0], rect)
            else:
                pg.draw.rect(self.screen, cl[1], rect)
            rect = (y * self.size/8, x * self.size/8, self.size/8, self.size/8)
            if (x + y) % 2:
                pg.draw.rect(self.screen, cl[0], rect)
            else:
                pg.draw.rect(self.screen, cl[1], rect)

        # Available moves
        for move in moves:
            if self.orientation:
                i = 7 - int(move[-2])
                j = 7 - int(move[-1])
                x = 7 - int(move[-4])
                y = 7 - int(move[-3])
            else:
                i = int(move[-2])
                j = int(move[-1])
                x = int(move[-4])
                y = int(move[-3])
            if board[x][y][-1] == str(self.orientation):
                cl = [colors['bottom_available_dark'], colors['bottom_available_light']]
            else:
                cl = [colors['top_available_dark'], colors['top_available_light']]
            rect = (j * self.size/8, i * self.size/8, self.size/8, self.size/8)
            
            if (i + j) % 2:
                pg.draw.rect(self.screen, cl[0], rect)
            else:
                pg.draw.rect(self.screen, cl[1], rect)
        
        

        # Pieces
        for i, row in enumerate(board):
            for j, piece in enumerate(row):
                if piece != '0' and piece != '1' and piece[-1] == '1':
                    if self.black_ai:
                        if piece[-2] == '1':
                            self.screen.blit(b_pawn_ai, (j * self.size/8, i * self.size/8))
                        if piece[-2] == '2':
                            self.screen.blit(b_bishop_ai, (j * self.size/8, i * self.size/8))
                        if piece[-2] == '3':
                            self.screen.blit(b_knight_ai, (j * self.size/8, i * self.size/8))
                        if piece[-2] == '4':
                            self.screen.blit(b_rook_ai, (j * self.size/8, i * self.size/8))
                        if piece[-2] == '5':
                            self.screen.blit(b_queen_ai, (j * self.size/8, i * self.size/8))
                        if piece[-2] == '6':
                            self.screen.blit(b_king_ai, (j * self.size/8, i * self.size/8))
                    else:
                        if piece[-2] == '1':
                            self.screen.blit(b_pawn, (j * self.size/8, i * self.size/8))
                        if piece[-2] == '2':
                            self.screen.blit(b_bishop, (j * self.size/8, i * self.size/8))
                        if piece[-2] == '3':
                            self.screen.blit(b_knight, (j * self.size/8, i * self.size/8))
                        if piece[-2] == '4':
                            self.screen.blit(b_rook, (j * self.size/8, i * self.size/8))
                        if piece[-2] == '5':
                            self.screen.blit(b_queen, (j * self.size/8, i * self.size/8))
                        if piece[-2] == '6':
                            self.screen.blit(b_king, (j * self.size/8, i * self.size/8))
                elif piece != '0' and piece != '1' and piece[-1] == '0':
                    if self.white_ai:
                        if piece[-2] == '1':
                            self.screen.blit(w_pawn_ai, (j * self.size/8, i * self.size/8))
                        if piece[-2] == '2':
                            self.screen.blit(w_bishop_ai, (j * self.size/8, i * self.size/8))
                        if piece[-2] == '3':
                            self.screen.blit(w_knight_ai, (j * self.size/8, i * self.size/8))
                        if piece[-2] == '4':
                            self.screen.blit(w_rook_ai, (j * self.size/8, i * self.size/8))
                        if piece[-2] == '5':
                            self.screen.blit(w_queen_ai, (j * self.size/8, i * self.size/8))
                        if piece[-2] == '6':
                            self.screen.blit(w_king_ai, (j * self.size/8, i * self.size/8))
                    else:
                        if piece[-2] == '1':
                            self.screen.blit(w_pawn, (j * self.size/8, i * self.size/8))
                        if piece[-2] == '2':
                            self.screen.blit(w_bishop, (j * self.size/8, i * self.size/8))
                        if piece[-2] == '3':
                            self.screen.blit(w_knight, (j * self.size/8, i * self.size/8))
                        if piece[-2] == '4':
                            self.screen.blit(w_rook, (j * self.size/8, i * self.size/8))
                        if piece[-2] == '5':
                            self.screen.blit(w_queen, (j * self.size/8, i * self.size/8))
                        if piece[-2] == '6':
                            self.screen.blit(w_king, (j * self.size/8, i * self.size/8))

        pg.display.flip()
