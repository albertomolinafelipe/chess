import pygame as pg
import os
import time
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

symbol_ai = pg.image.load(os.path.join("img", "symbol_ai.png"))
symbol_user = pg.image.load(os.path.join("img", "symbol_user.png"))
king_both = pg.image.load(os.path.join("img", "symbol_user.png"))

palette = {
    'dark_tile' : (107, 74, 49),
    'light_tile' : (212, 202, 183),

    'selected_light' : (226, 78, 75),
    'selected_dark' : (234, 81, 81),

    'available_move_p1_light' : (121, 172, 109),
    'available_move_p1_dark' : (92, 142, 84),
    'available_move_p2_light' : (106, 151, 174),
    'available_move_p2_dark' : (71, 133, 173),
}

class UserInterface:
    def __init__(self) -> None:
        self.last_move = None
        self.size = 480

        pg.init()
        self.font = pg.font.SysFont('couriernew.ttf', 40) 
        self.screen = pg.display.set_mode((480, 480))

    def getUserInfo(self):
        """ Get how players and colors """

        state = 0 # Dont have player info or color

        while True:
            self.drawUserInfoSelection(state)

            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    py = event.pos[0]
                    if not state:
                        if py < self.size//3:
                            self.user_info = [None, None]
                            state += 1
                        elif py < 2*self.size//3:
                            self.user_info = [None]
                            state += 1
                        else:
                            self.user_info = [1]
                            return [None]
                    else:
                        if py < self.size//3:
                            self.user_info[0] = 1
                            if len(self.user_info) > 1:
                                self.user_info[1] = 0
                        elif py < 2*self.size//3:
                            if np.random.random() < .5:
                                self.user_info[0] = 1
                                if len(self.user_info) > 1:
                                    self.user_info[1] = 0
                            else:
                                self.user_info[0] = 0
                                if len(self.user_info) > 1:
                                    self.user_info[1] = 1
                        else:
                            self.user_info[0] = 0
                            if len(self.user_info) > 1:
                                self.user_info[1] = 1
                        return self.user_info

                if event.type == pg.QUIT:
                    pg.quit()
                    return -1

    def drawUserInfoSelection(self, state):
        """ Draw selection menu """
        left_rect = (0, 0, self.size/3, self.size)
        mid_rect = (self.size/3, 0, self.size/3, self.size)
        right_rect = (2*self.size/3, 0, self.size/3, self.size)
        if not state:
            self.screen.fill((80, 80, 80))

            pg.draw.rect(self.screen, palette["light_tile"], left_rect, 1)
            pg.draw.rect(self.screen, palette["light_tile"], mid_rect, 1)
            pg.draw.rect(self.screen, palette["light_tile"], right_rect, 1)

            vs = self.font.render('vs.', True, (255,255,255))

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
            pg.draw.rect(self.screen, (230,230,230), left_rect)
            pg.draw.rect(self.screen, (120,120,120), mid_rect)
            pg.draw.rect(self.screen, (50,50,50), right_rect)

            self.screen.blit(b_king, (int(self.size/6 - 30), int(self.size/2) - 25))
            self.screen.blit(king_both, (int(self.size/2 - 30), int(self.size/2) - 25))
            self.screen.blit(w_king, (int(5*self.size/6 - 30), int(self.size/2) - 25))

        pg.display.flip()


    def display(self, board_, all_moves, last_move, selection=False, end=False):
        """ Get coordinates of  """
        selected = None
        possible_moves = []
        turn = board_[-1][-2]
        losser = board_[-1][-2]

        if board_[-1][-1] != 3 and not end:
            return 0

        if turn:
            same_color = range(6)
        else:
            same_color = range(6, 12)

        board = self.boardToMatrix(board_)

        start = time.time()
        cond = True
        while cond:
            if not selection:
                cond = time.time() < start + .25
            self.drawBoard(board, selected, possible_moves, last_move, turn)
            if not end:
                if turn :
                    pg.display.set_caption("CHESS_3: BLACK MOVES")
                else:
                    pg.display.set_caption("CHESS_3: WHITE MOVES")
            else:
                if losser == 1:
                    pg.display.set_caption("-- WHITE WINS --")
                elif losser == 0:
                    pg.display.set_caption("-- BLACK WINS --")
                else:
                    pg.display.set_caption("-- DRAW --")
            for event in pg.event.get():
                
                # Click
                if event.type == pg.MOUSEBUTTONDOWN:
                    col = int(event.pos[0]//(self.size/8))
                    row = int(event.pos[1]//(self.size/8))

                    if selection and not end:
                        if board[row][col] in same_color:
                            selected = [row, col]
                            possible_moves = []
                            for move in all_moves:
                                if self.user_info[0]:
                                    if (7 - row) * 8 + (7 - col)  == move[0]:
                                        possible_moves.append(move)
                                elif row * 8 + col == move[0]:
                                        possible_moves.append(move)

                    if selected is not None:
                        for move in possible_moves:
                            if self.user_info[0]:
                                if (7 - row) * 8 + (7 - col) == move[1]:
                                    return move
                            elif row * 8 + col == move[1]:
                                    return move

                if event.type == pg.QUIT:
                    pg.quit()
                    return -1

    def drawBoard(self, board, selected, possible_moves, last_move, turn):
        """ Shows board
            - All_moves are all the available moves for the user to choose with piece selected
            - Selected piece
            - Last move made, shown as well
            - Time, show the board for time seconds
            """

        for i, row in enumerate(board):
            for j, tile in enumerate(row):
                rect = (j * self.size/8, i * self.size/8, self.size/8, self.size/8)
                if (i + j) % 2:
                    pg.draw.rect(self.screen, palette['dark_tile'], rect)
                else:
                    pg.draw.rect(self.screen, palette['light_tile'], rect)

                if selected is not None and [i, j] == selected:
                    if (i + j) % 2:
                        pg.draw.rect(self.screen, palette['selected_dark'], rect)
                    else:
                        pg.draw.rect(self.screen, palette['selected_light'], rect)

        for position in last_move:
            if self.user_info[0]:
                i = 7 - (position // 8)
                j = 7 - (position % 8)
            else:
                i = position // 8
                j = position % 8
            rect = (j * self.size/8, i * self.size/8, self.size/8, self.size/8)
            if turn != self.user_info[0]:
                if (i + j) % 2:
                    pg.draw.rect(self.screen, palette['available_move_p1_dark'], rect)
                else:
                    pg.draw.rect(self.screen, palette['available_move_p1_light'], rect)
            else:
                if (i + j) % 2:
                    pg.draw.rect(self.screen, palette['available_move_p2_dark'], rect)
                else:
                    pg.draw.rect(self.screen, palette['available_move_p2_light'], rect)
        
        
        for move in possible_moves:
            if self.user_info[0]:
                i = 7 - (move[1] // 8)
                j = 7 - (move[1] % 8)
            else:
                i = move[1] // 8
                j = move[1] % 8
            rect = (j * self.size/8, i * self.size/8, self.size/8, self.size/8)
            if turn == self.user_info[0]:
                if (i + j) % 2:
                    pg.draw.rect(self.screen, palette['available_move_p1_dark'], rect)
                else:
                    pg.draw.rect(self.screen, palette['available_move_p1_light'], rect)
            else:
                if (i + j) % 2:
                    pg.draw.rect(self.screen, palette['available_move_p2_dark'], rect)
                else:
                    pg.draw.rect(self.screen, palette['available_move_p2_light'], rect)

        


        for i, row in enumerate(board):
            for j, tile in enumerate(row):
                pos = (j * self.size/8, i * self.size/8)

                if tile == 0:
                    self.screen.blit(b_pawn, pos)
                if tile == 1:
                    self.screen.blit(b_knight, pos)
                if tile == 2:
                    self.screen.blit(b_bishop, pos)
                if tile == 3:
                    self.screen.blit(b_rook, pos)
                if tile == 4:
                    self.screen.blit(b_queen, pos)
                if tile == 5:
                    self.screen.blit(b_king, pos)

                if tile == 6:
                    self.screen.blit(w_pawn, pos)
                if tile == 7:
                    self.screen.blit(w_knight, pos)
                if tile == 8:
                    self.screen.blit(w_bishop, pos)
                if tile == 9:
                    self.screen.blit(w_rook, pos)
                if tile == 10:
                    self.screen.blit(w_queen, pos)
                if tile == 11:
                    self.screen.blit(w_king, pos)
                

        pg.display.flip()

    def boardToMatrix(self, board):
        matrix = [[-1 for x in range(8)] for y in range(8)]
        for piece_index, piece_group in enumerate(board[:-1]):
            for piece in piece_group:
                if piece:
                    piece_pos = 66 - len(bin(piece))
                    matrix[piece_pos//8][piece_pos%8] = piece_index

        # If its blacks turn and black is player 1, bottom

        if self.user_info[0]:
            matrix = np.rot90(matrix, k=2, axes=(1, 0))

        return matrix