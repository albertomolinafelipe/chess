import random
import pygame as pg
import os
import time
import numpy as np

b_pawn = pg.transform.smoothscale(pg.image.load(os.path.join("img", "b_pawn.png")), (60, 60))
b_knight = pg.transform.smoothscale(pg.image.load(os.path.join("img", "b_knight.png")), (60, 60))
b_bishop = pg.transform.smoothscale(pg.image.load(os.path.join("img", "b_bishop.png")), (60, 60))
b_rook = pg.transform.smoothscale(pg.image.load(os.path.join("img", "b_rook.png")), (60, 60))
b_queen = pg.transform.smoothscale(pg.image.load(os.path.join("img", "b_queen.png")), (60, 60))
b_king = pg.transform.smoothscale(pg.image.load(os.path.join("img", "b_king.png")), (60, 60))

w_pawn = pg.transform.smoothscale(pg.image.load(os.path.join("img", "w_pawn.png")), (60, 60))
w_knight = pg.transform.smoothscale(pg.image.load(os.path.join("img", "w_knight.png")), (60, 60))
w_bishop = pg.transform.smoothscale(pg.image.load(os.path.join("img", "w_bishop.png")), (60, 60))
w_rook = pg.transform.smoothscale(pg.image.load(os.path.join("img", "w_rook.png")), (60, 60))
w_queen = pg.transform.smoothscale(pg.image.load(os.path.join("img", "w_queen.png")), (60, 60))
w_king = pg.transform.smoothscale(pg.image.load(os.path.join("img", "w_king.png")), (60, 60))

symbol_ai = pg.image.load(os.path.join("img", "symbol_ai.png"))
symbol_user = pg.image.load(os.path.join("img", "symbol_user.png"))
symbol_rewind = pg.transform.smoothscale(pg.image.load(os.path.join("img", "symbol_rewind.png")), (40, 29))
symbol_ffoward = pg.transform.smoothscale(pg.image.load(os.path.join("img", "symbol_ffoward.png")), (40, 29))
symbol_king = pg.transform.smoothscale(pg.image.load(os.path.join("img", "symbol_king.png")), (60, 60))
symbol_dice = pg.transform.smoothscale(pg.image.load(os.path.join("img", "symbol_dice.png")), (60, 60))
symbol_search = pg.transform.smoothscale(pg.image.load(os.path.join("img", "symbol_search.png")), (60, 60))
symbol_gear = pg.transform.smoothscale(pg.image.load(os.path.join("img", "symbol_gear.png")), (20, 20))
symbol_gear_sel = pg.transform.smoothscale(pg.image.load(os.path.join("img", "symbol_gear_sel.png")), (20, 20))

piece_images = [w_pawn, w_knight, w_bishop, w_rook, w_queen, w_king, None, None, b_pawn, b_knight, b_bishop, b_rook, b_queen, b_king]

colors = {

    'background' : (30, 30, 30),

    'white' : (255, 255, 255),

    'choose_user' : (50, 50, 50),

    'choose_black' : (200, 200, 200),
    'choose_random' : (100, 100, 100),
    'choose_white' : (50, 50, 50),

    'dark_tile' : (117, 78, 55),
    'light_tile' : (217, 195, 176),

    'selected_light' : (226, 78, 75),
    'selected_dark' : (234, 81, 81),
    'last_move_dark' : (103, 151, 108),
    'last_move_light' : (115, 167, 119),
    'options' : (96, 181, 103),

    'aidiag_dark' : (247,105,24),
    'aidiag_light1' : (255,137,70),
    'aidiag_light2' : (254,156,101),
    'aidiag_grey' : (59, 59, 59),


}

width = 820
height = 540

boardWidth = 480
boardHeight = 480
margin = 30

pregameButtonWidth = 250
pregameButtonHeight = 140

aiSettingsTextX = margin + boardWidth + margin + 8
aiSettingsText1Y = margin + 12
aiSettingsText2Y = aiSettingsText1Y + 35
aiSettingsTextBoxX = margin + boardWidth + margin
aiSettingsTextBoxY = margin
aiSettingsTextBoxH = 75

aiSettingsW = 250
aiSettingsH = (height - aiSettingsTextBoxH - 4*margin)//2
aiSettingsBox1X = margin + boardWidth + margin
aiSettingsBox1Y = margin + aiSettingsTextBoxH + margin
aiSettingsBox2Y = aiSettingsBox1Y + aiSettingsH + margin

pregameBX = margin+boardWidth+margin
pregameB1Y = margin
pregameB2Y = margin+pregameButtonHeight+margin
pregameB3Y = margin+pregameButtonHeight+margin+pregameButtonHeight+margin

userSymbolYMargin = 38
userSymbolWidth = 64
userSymbol1Y = margin+userSymbolYMargin
userSymbol2Y = userSymbol1Y+margin+pregameButtonHeight
userSymbol3Y = userSymbol2Y+margin+pregameButtonHeight
userSymbolLeftX = margin+boardWidth+margin+margin
userSymbolRightX = margin+boardWidth+margin+pregameButtonWidth-userSymbolWidth-margin
vsX = userSymbolLeftX+userSymbolWidth+20
vs1Y = margin+60
vs2Y = vs1Y+pregameButtonHeight+margin
vs3Y = vs2Y+pregameButtonHeight+margin

arrowBoxX = margin + boardHeight + margin
arrowBoxY = height - margin - 60
arrowBoxW = width - arrowBoxX  - margin
arrowBoxH = 60

choosePromotionX = margin+boardWidth+margin
choosePromotionY = arrowBoxY - 10 - 60
choosePromotionW = arrowBoxW
choosePromotionH = 60

colorSymbolX = pregameBX+95
colorSymbol1Y = margin+40
colorSymbol2Y = colorSymbol1Y+pregameButtonHeight+margin
colorSymbol3Y = colorSymbol2Y+pregameButtonHeight+margin

aiDiagSymbolX = 540
aiDiagSymbolY = 30
aiDiagTitleX = 610
aiDiagTitleY = 53

aiDiagTextX = 555

aiDiagModes1Y = 110
aiDiagModes2Y = aiDiagModes1Y + 1*25
aiDiagModes3Y = aiDiagModes1Y + 2*25

aiDiagText1Y = 200
aiDiagText2Y = aiDiagText1Y + 1*25
aiDiagText3Y = aiDiagText1Y + 2*25

debugX = 480+30+30
debugY = 30
debugW = width-480-30-30-30
debugH = height-2*margin-60-margin

class UI:

    def __init__(self):
        self.board_stack = []
        self.moves_stack = []
        self.ai_diag = ['-'] * 6
        self.stack_index = 0

        self.clicked = -1
        self.piece_dragged = -1  # position
        
        self.debug_info_stack = []
        self.debug = False
        self.debug_options = [False for i in range(3)]
        
        self.orientation = 0
        self.ai_player = False

        pg.init()
        self.fonts = [pg.font.SysFont('couriernew.ttf', 35), pg.font.SysFont('couriernew.ttf', 24), pg.font.SysFont('couriernew.ttf', 22)]
        self.screen = pg.display.set_mode((820, 540))

    def getPreGame(self, board) -> list:
        """
        0: PvP, PvAI, AIvAI

        1: AI settings for 1/1 AI
        2: AI advanced settings for 1/1 AI

        3: Ai settings for 1/2 AI
        4: AI advanced settings for 1/2 AI
        5: Ai settings for 2/2 AI
        6: AI advanced settings for 2/2 AI

        7, colors
        
        """
        pregame = 0
        run = True
        ai_settings = [None, None]
        ai_colors = []


        while run:
            self.draw(board, pregame=pregame)

            pg.display.set_caption('[Chess Engine 4.0.0]')

            for event in pg.event.get():

                if event.type == pg.MOUSEBUTTONDOWN:
                    px = event.pos[0]
                    py = event.pos[1]


                    if pregame == 0:

                        if pregameBX <= px <= pregameBX+pregameButtonWidth:
                            if pregameB1Y <= py <= pregameB1Y+pregameButtonHeight: # player vs player
                                pregame = 7

                            if pregameB2Y <= py <= pregameB2Y+pregameButtonHeight: # player vs AI
                                self.ai_player = True
                                pregame = 1

                            if pregameB3Y <= py <= pregameB3Y+pregameButtonHeight: # AI vs AI
                                self.ai_player = True
                                ai_colors = [0, 1]
                                pregame = 3


                    elif pregame in [1, 3, 5]:
                        click = 0

                        if aiSettingsTextBoxX + aiSettingsW - 20 - 5 - 5 < px < aiSettingsTextBoxX + aiSettingsW and\
                            aiSettingsTextBoxY + aiSettingsTextBoxH - 20 - 5 - 5 < py <  aiSettingsTextBoxY + aiSettingsTextBoxH:
                            pregame += 1

                        if aiSettingsBox1X < px < aiSettingsBox1X + aiSettingsW:
                            if aiSettingsBox1Y < py < aiSettingsBox1Y + aiSettingsH:
                                click = 1
                            if aiSettingsBox2Y < py < aiSettingsBox2Y + aiSettingsH:
                                click = 2

                        if click:
                            if pregame == 1:
                                ai_settings = [click, click]
                                pregame = 7

                            elif pregame == 3:
                                ai_settings[0] = click
                                pregame = 5

                            elif pregame == 5:
                                ai_settings[1] = click
                                return ai_settings, ai_colors
 

                    elif pregame in [2, 4, 6]:
                        if aiSettingsTextBoxX + aiSettingsW - 20 - 5 - 5 < px < aiSettingsTextBoxX + aiSettingsW and\
                            aiSettingsTextBoxY + aiSettingsTextBoxH - 20 - 5 - 5 < py <  aiSettingsTextBoxY + aiSettingsTextBoxH:
                            pregame -= 1

                    elif pregame == 7:

                        if pregameBX <= px <= pregameBX+pregameButtonWidth:

                            if pregameB1Y <= py <= pregameB1Y+pregameButtonHeight: # black
                                self.orientation = True
                                ai_colors = [0] if self.ai_player else []
                                ai_settings[1] = None
                                return ai_settings, ai_colors


                            if pregameB2Y <= py <= pregameB2Y+pregameButtonHeight: # random
                                if random.random() > 0.5:
                                    self.orientation = True
                                    ai_colors = [0] if self.ai_player else []
                                    ai_settings[1] = None
                                else:
                                    ai_colors = [1] if self.ai_player else []
                                    ai_settings[0] = None
                                return ai_settings, ai_colors

                            if pregameB3Y <= py <= pregameB3Y+pregameButtonHeight: # white
                                ai_colors = [1] if self.ai_player else []
                                ai_settings[0] = None
                                return ai_settings, ai_colors


                if event.type == pg.QUIT:
                    pg.quit()
                    return -1, -1

    def display(self, board, 
                          turn, 
                          move=[], 
                          selection=False, 
                          all_moves=[], 
                          board_debug=None, 
                          result=None, 
                          ai_diag=None):

        start = time.time()

        if selection:
            self.handleStacks(board, move, len(all_moves), board_debug)
            last_board_index = self.stack_index
        else:
            last_board_index = np.inf
            # turn board around
            if self.orientation:
                board.reverse()

        if ai_diag is not None:
            self.ai_diag = ai_diag

        selected = None
        selected_piece_moves_to_draw = []
        selected_piece_moves = []
        same_color_piece_indeces = range(9, 15) if turn else range(1, 7)
        
        choose_promotion = []
        self.piece_dragged = -1
        self.clicked = -1


        run = True
        while run:
            self.draw(board_matrix=self.board_stack[self.stack_index], 
                    turn=turn, 
                    move=self.moves_stack[self.stack_index],
                    selected=selected, 
                    selected_piece_moves=selected_piece_moves_to_draw, 
                    rewind=self.stack_index > 0,
                    ffoward=self.stack_index < last_board_index,
                    choose_promotion=len(choose_promotion),
                    result=result)

            pg.display.set_caption('[Chess Engine 4.0.0]')

            # if only displaying
            if not selection and time.time() > start + .1:
                return 0

            for event in pg.event.get():
                
                if selection:

                    # Rewind and Ffoward with arrow keys
                    if event.type == pg.KEYDOWN:

                        if event.key == pg.K_LEFT and self.stack_index > 0:
                            self.stack_index -= 1
                            selected = None
                            selected_piece_moves = []
                            selected_piece_moves_to_draw = []

                        if event.key == pg.K_RIGHT and self.stack_index < last_board_index:
                            self.stack_index += 1

                        if event.key == pg.K_UP:
                            self.stack_index = last_board_index

                        if event.key == pg.K_DOWN:
                            self.stack_index = 0

                        if event.key == pg.K_SPACE:
                            self.debug = not self.debug
                        if self.debug:
                            if event.key == pg.K_a:
                                self.debug_options[0] = not self.debug_options[0]
                            if event.key == pg.K_p:
                                self.debug_options[1] = not self.debug_options[1]
                            if event.key == pg.K_c:
                                self.debug_options[2] = not self.debug_options[2]

                    if self.clicked == 1 and event.type == pg.MOUSEBUTTONUP:
                        self.clicked = 0
                        self.piece_dragged = -1

                        px = event.pos[0]
                        py = event.pos[1]

                        row = (py - margin) // 60
                        col = (px - margin) // 60

                        # if let go outside
                        if not 0 <= py-margin <= boardHeight or not 0 <= px-margin <= boardHeight:
                            selected = []
                            choose_promotion = []
                            selected_piece_moves = []
                            selected_piece_moves_to_draw = []         
                    
                        else:
                            if self.orientation:
                                row = 7 - row
                                col = 7 - col
                            for move in selected_piece_moves:
                                if row*8 + col == move[1]:
                                    if move[2] != 2:
                                        return move
                                    else:
                                        choose_promotion.append(move)

                    if event.type == pg.MOUSEBUTTONDOWN:

                        self.clicked = 1

                        px = event.pos[0]
                        py = event.pos[1]

                        if len(choose_promotion) and choosePromotionY <= py <= choosePromotionY+choosePromotionH:

                            if choosePromotionX <= px <= choosePromotionX + choosePromotionW//2:
                                return choose_promotion[1] 
                            
                            if choosePromotionX + choosePromotionW//2 <= px <= choosePromotionX + choosePromotionW:
                                return choose_promotion[0] 


                        # Rewind and ffoward with buttons
                        if arrowBoxY <= py <= arrowBoxY+arrowBoxH:
                            # Back
                            if arrowBoxX <= px <= arrowBoxX+arrowBoxW/2 and self.stack_index > 0:
                                self.stack_index -= 1
                                selected = None
                                selected_piece_moves = []
                                selected_piece_moves_to_draw = []
                            # Foward
                            if arrowBoxX+arrowBoxW/2 <= px <= arrowBoxX+arrowBoxW and self.stack_index < last_board_index:
                                self.stack_index += 1

                        # If we are on the LAST stack, we can choose and move
                        if self.stack_index == last_board_index:
                            
                            # Inside the board coordinates
                            if 0 <= py-margin <= boardHeight and 0 <= px-margin <= boardHeight:
                                
                                row = (py - margin) // 60
                                col = (px - margin) // 60
                                
                                if board[row*8 + col] in same_color_piece_indeces:

                                    self.piece_dragged = row*8 + col

                                    selected = row*8 + col
                                    choose_promotion = []
                                    selected_piece_moves = []
                                    selected_piece_moves_to_draw = []

                                    # If black is at the bottom change the coords
                                    if self.orientation:
                                            row = 7 - row
                                            col = 7 - col

                                    # Get moves to highlight
                                    for move in all_moves:

                                        if move[0] == row*8 + col:
                                            if self.orientation:
                                                selected_piece_moves_to_draw.append(63 - move[1])
                                            else:
                                                selected_piece_moves_to_draw.append(move[1])
                                            selected_piece_moves.append(move)

                                elif selected is not None:
                                    if self.orientation:
                                            row = 7 - row
                                            col = 7 - col
                                    for move in selected_piece_moves:
                                        if row*8 + col == move[1]:
                                            if move[2] != 2:
                                                return move
                                            else:
                                                choose_promotion.append(move)


                if event.type == pg.QUIT:
                    pg.quit()
                    run = False
                    return -1
        
    def draw(self, board_matrix, 
                   turn=None, 
                   move=[],
                   selected=[],
                   selected_piece_moves=[], 
                   pregame=None, 
                   rewind=None, 
                   ffoward=None,
                   choose_promotion=False,
                   result=None):

        self.screen.fill(colors['background'])
        mouse = pg.mouse.get_pos()
        mouse_row = (mouse[1] - margin) // 60
        mouse_col = (mouse[0] - margin) // 60


        if pregame is None:

            if self.debug:
                self.drawDebug()

            elif self.ai_player:
                self.drawAiDiag()

            if choose_promotion:
                self.drawPromotion(turn)

            self.drawRewind(rewind, ffoward)

            if result is not None:
                self.drawResult(turn, result)
 
        else:
            self.drawPregame(pregame, mouse)
            
        # Draw board
        for x, tile in enumerate(board_matrix):

            i = x // 8
            j = x % 8

            rect = (j * 60 + 30, i * 60 + 30, 60, 60)
            center = ((j + 1) * 60, (i + 1) * 60)


            # TILES

            if (i+j) % 2: # dark tile
                pg.draw.rect(self.screen, colors['dark_tile'], rect)
            else: # light tile
                pg.draw.rect(self.screen, colors['light_tile'], rect)


            if self.debug_options[0] and (1 << x) & self.debug_info_stack[self.stack_index][7]:
                if (i+j) % 2: 
                    pg.draw.rect(self.screen, (255,0,0), rect)
                else: 
                    pg.draw.rect(self.screen, (255,128,128), rect)

            if self.debug_options[1] and (1 << x) & self.debug_info_stack[self.stack_index][8]:
                if (i+j) % 2: 
                    pg.draw.rect(self.screen, (0,0,255), rect)
                else: 
                    pg.draw.rect(self.screen, (128,128,255), rect)

            if self.debug_options[2] and (1 << x) & self.debug_info_stack[self.stack_index][9]:
                if (i+j) % 2: 
                    pg.draw.rect(self.screen, (0,255,0), rect)
                else: 
                    pg.draw.rect(self.screen, (128,255,128), rect)


            # SELECTEC PIECE
            if x == selected:
                if (i+j) % 2: 
                    pg.draw.polygon(self.screen, colors['selected_dark'], ((j * 60 + 30, i * 60 + 30), (j * 60 + 30 + 15, i * 60 + 30), (j * 60 + 30, i * 60 + 30 + 15)))
                    pg.draw.polygon(self.screen, colors['selected_dark'], (((j+1) * 60 + 30, i * 60 + 30), ((j+1) * 60 + 30 - 15, i * 60 + 30), ((j+1) * 60 + 30, i * 60 + 30 + 15)))
                    pg.draw.polygon(self.screen, colors['selected_dark'], (((j+1) * 60 + 30, (i+1) * 60 + 30), ((j+1) * 60 + 30 - 15, (i+1) * 60 + 30), ((j+1) * 60 + 30, (i+1) * 60 + 30 - 15)))
                    pg.draw.polygon(self.screen, colors['selected_dark'], ((j * 60 + 30, (i+1) * 60 + 30), (j * 60 + 30, (i+1) * 60 + 30 - 15), (j * 60 + 30 + 15, (i+1) * 60 + 30)))
                else: 
                    pg.draw.polygon(self.screen, colors['selected_light'], ((j * 60 + 30, i * 60 + 30), (j * 60 + 30 + 15, i * 60 + 30), (j * 60 + 30, i * 60 + 30 + 15)))
                    pg.draw.polygon(self.screen, colors['selected_light'], (((j+1) * 60 + 30, i * 60 + 30), ((j+1) * 60 + 30 - 15, i * 60 + 30), ((j+1) * 60 + 30, i * 60 + 30 + 15)))
                    pg.draw.polygon(self.screen, colors['selected_light'], (((j+1) * 60 + 30, (i+1) * 60 + 30), ((j+1) * 60 + 30 - 15, (i+1) * 60 + 30), ((j+1) * 60 + 30, (i+1) * 60 + 30 - 15)))
                    pg.draw.polygon(self.screen, colors['selected_light'], ((j * 60 + 30, (i+1) * 60 + 30), (j * 60 + 30, (i+1) * 60 + 30 - 15), (j * 60 + 30 + 15, (i+1) * 60 + 30)))


            # LAST MoVE
            if not self.debug and x in move[:2] and x not in selected_piece_moves:
                if (i+j) % 2: 
                    pg.draw.rect(self.screen, colors['last_move_dark'], rect)
                else: 
                    pg.draw.rect(self.screen, colors['last_move_light'], rect)
            

            # OPTIONS
            if x in selected_piece_moves:
                if mouse_row * 8 + mouse_col == x:
                    pg.draw.rect(self.screen, colors['options'], rect)
                elif board_matrix[x]:
                    pg.draw.polygon(self.screen, colors['options'], ((j * 60 + 30, i * 60 + 30), (j * 60 + 30 + 15, i * 60 + 30), (j * 60 + 30, i * 60 + 30 + 15)))
                    pg.draw.polygon(self.screen, colors['options'], (((j+1) * 60 + 30, i * 60 + 30), ((j+1) * 60 + 30 - 15, i * 60 + 30), ((j+1) * 60 + 30, i * 60 + 30 + 15)))
                    pg.draw.polygon(self.screen, colors['options'], (((j+1) * 60 + 30, (i+1) * 60 + 30), ((j+1) * 60 + 30 - 15, (i+1) * 60 + 30), ((j+1) * 60 + 30, (i+1) * 60 + 30 - 15)))
                    pg.draw.polygon(self.screen, colors['options'], ((j * 60 + 30, (i+1) * 60 + 30), (j * 60 + 30, (i+1) * 60 + 30 - 15), (j * 60 + 30 + 15, (i+1) * 60 + 30)))
                else:                        
                    pg.draw.circle(self.screen, colors['options'], center, 8)
        

            if tile and (x != self.piece_dragged or 8 * mouse_row + mouse_col == x):
                self.screen.blit(piece_images[tile-1], (j * 60 + 30, i * 60 + 30))

        # DRAGGED PIECE
        if self.piece_dragged != -1 and 8 * mouse_row + mouse_col!=self.piece_dragged:
            self.screen.blit(piece_images[board_matrix[self.piece_dragged]-1], (pg.mouse.get_pos()[0]-30, pg.mouse.get_pos()[1]-30))


        pg.display.flip()

    def handleDebug(self, all_moves, board_debug):

        new = []
        new.append(all_moves)                              # possible moves
        new.append(board_debug.game_state_stack[-1] & 15)          # piece taken
        new.append(board_debug.move_gen.check)                # check
        new.append((board_debug.game_state_stack[-1] >> 4) & 15)   # castling
        new.append(board_debug.game_state_stack[-1] >> 13)         # draw move
        new.append(board_debug.move_counter)                  # move counter
        new.append((board_debug.game_state_stack[-1] >> 9) & 15)   # en passant
        new.append(board_debug.move_gen.attack_map)           # attack map
        new.append(board_debug.move_gen.pin_ray_map)          # pin map
        new.append(board_debug.move_gen.check_map)            # check map

        self.debug_info_stack.append(new)

    def handleStacks(self, board, move, all_moves, board_debug):

        if self.orientation:
            board.reverse()

        self.board_stack.append(board)

        if self.orientation and len(move):
            self.moves_stack.append([63-move[0], 63-move[1],0])
        else:
            self.moves_stack.append(move)

        self.stack_index = len(self.board_stack) - 1

        self.handleDebug(all_moves, board_debug)

    def drawAiDiag(self):
        self.screen.blit(symbol_ai, (aiDiagSymbolX, aiDiagSymbolY))
        title = self.fonts[0].render('AI Diagnostics', True, colors['aidiag_dark'])


        time = self.fonts[1].render(f'time: {self.ai_diag[0]}', True, colors['aidiag_light2'])
        depth = self.fonts[1].render(f'depth: {self.ai_diag[1]} moves', True, colors['aidiag_light2'])
        positions = self.fonts[1].render(f'positions checked: {self.ai_diag[2]}', True, colors['aidiag_light2'])


        alpha = self.fonts[2].render(f'Alpha-beta pruning: {self.ai_diag[3]}', True, colors['aidiag_grey'])
        montecarlo = self.fonts[2].render(f'Monte-Carlo search {self.ai_diag[4]}', True, colors['aidiag_light1'])
        zobrist = self.fonts[2].render(f'Zobrist hashing: {self.ai_diag[5]}', True, colors['aidiag_light1'])
        

        self.screen.blit(title, (aiDiagTitleX, aiDiagTitleY))


        self.screen.blit(time, (aiDiagTextX, aiDiagText1Y))
        self.screen.blit(depth, (aiDiagTextX, aiDiagText2Y))
        self.screen.blit(positions, (aiDiagTextX, aiDiagText3Y))


        self.screen.blit(alpha, (aiDiagTextX, aiDiagModes1Y))
        self.screen.blit(montecarlo, (aiDiagTextX, aiDiagModes2Y))
        self.screen.blit(zobrist, (aiDiagTextX, aiDiagModes3Y))

    def drawDebug(self):
        pg.draw.rect(self.screen, (70, 70, 70), (debugX, debugY, debugW, debugH))
        pg.draw.rect(self.screen, (128, 255, 128), (debugX, debugY, debugW, debugH), 1)

        _possible_moves = self.fonts[2].render(f'Possible moves = { self.debug_info_stack[self.stack_index][0]}', True, colors['options'])
        _taken = self.fonts[2].render(f'Piece taken = {             self.debug_info_stack[self.stack_index][1]}', True, colors['options'])
        _check = self.fonts[2].render(f'Check = {                   self.debug_info_stack[self.stack_index][2]}', True, colors['options'])
        _castling = self.fonts[2].render(f'Castling KQkq = {        bin(self.debug_info_stack[self.stack_index][3])}', True, colors['options'])
        _draw_move = self.fonts[2].render(f'Draw moves = {          self.debug_info_stack[self.stack_index][4]}', True, colors['options'])
        _move_counter = self.fonts[2].render(f'Move counter = {     self.debug_info_stack[self.stack_index][5]}', True, colors['options'])
        _en_passant = self.fonts[2].render(f'En passant = {         self.debug_info_stack[self.stack_index][6]-8}', True, colors['options'])
        _attack_map = self.fonts[2].render(f'Attack Map (A) = {     self.debug_options[0]}', True, colors['options'])
        _pin_map = self.fonts[2].render(f'Pin Map (P) = {           self.debug_options[1]}', True, colors['options'])
        _check_map = self.fonts[2].render(f'Check Map (C) = {       self.debug_options[2]}', True, colors['options'])
        str_list = [_possible_moves, _taken, _check, _castling, _draw_move, _move_counter, _en_passant, _attack_map, _pin_map, _check_map]

        for i in range(len(str_list)):
            self.screen.blit(str_list[i], (debugX + 10, debugY + i*30 + 8))
            pg.draw.rect(self.screen, (128, 255, 128), (debugX, debugY+i*30, debugW, 30), 1)

    def drawPromotion(self, turn):
        pg.draw.rect(self.screen, colors['choose_random'], (choosePromotionX,choosePromotionY,choosePromotionW,choosePromotionH))
        pg.draw.line(self.screen, colors['background'], (choosePromotionX+choosePromotionW//2, choosePromotionY + 10), (choosePromotionX+choosePromotionW//2, choosePromotionY + choosePromotionH - 10), 3)
        
        if turn:
            self.screen.blit(b_queen, (choosePromotionX + (choosePromotionW//2-60)//2, choosePromotionY))
            self.screen.blit(b_knight, (choosePromotionX + choosePromotionW//2 +(choosePromotionW//2-60)//2, choosePromotionY))
        else:
            self.screen.blit(w_queen, (choosePromotionX + (choosePromotionW//2-60)//2, choosePromotionY))
            self.screen.blit(w_knight, (choosePromotionX + choosePromotionW//2 + (choosePromotionW//2-60)//2, choosePromotionY))

    def drawRewind(self, rewind, ffoward):
        pg.draw.rect(self.screen, colors['choose_white'], (arrowBoxX, arrowBoxY, arrowBoxW, arrowBoxH))
        pg.draw.line(self.screen, colors['background'], (arrowBoxX+arrowBoxW//2, arrowBoxY + 10), (arrowBoxX+arrowBoxW//2, arrowBoxY + arrowBoxH - 10), 3)
        if rewind:
            self.screen.blit(symbol_rewind, (arrowBoxX + (arrowBoxW//2 - 40)//2, arrowBoxY + (arrowBoxH-29)//2))
        if ffoward:
            self.screen.blit(symbol_ffoward, (arrowBoxX + (arrowBoxW//2 - 40)//2 + arrowBoxW//2, arrowBoxY + (arrowBoxH-29)//2))

    def drawResult(self, turn, result):
        turn_color = 'BLANCAS' if turn else 'NEGRAS'
        pg.draw.rect(self.screen, colors['choose_random'], (choosePromotionX,choosePromotionY,choosePromotionW,choosePromotionH))
        if result == -1:
            result_string = self.fonts[0].render(f'GANAN {turn_color}', True, colors['aidiag_dark'])
            self.screen.blit(result_string, (choosePromotionX + 18, choosePromotionY + 20))
        if result == 1:
            result_string = self.fonts[0].render(f'EMPATE', True, colors['aidiag_dark'])
            self.screen.blit(result_string, (choosePromotionX + 18, choosePromotionY + 20))

    def drawPregame(self, pregame, mouse):
        if pregame == 0:
            pg.draw.rect(self.screen, colors['choose_user'], (pregameBX, pregameB1Y, pregameButtonWidth, pregameButtonHeight))
            pg.draw.rect(self.screen, colors['choose_user'], (pregameBX, pregameB2Y, pregameButtonWidth, pregameButtonHeight))
            pg.draw.rect(self.screen, colors['choose_user'], (pregameBX, pregameB3Y, pregameButtonWidth, pregameButtonHeight))

            vs = self.fonts[0].render('vs', True, colors['white'])

            self.screen.blit(symbol_user, (userSymbolLeftX, userSymbol1Y))
            self.screen.blit(vs, (vsX, vs1Y))
            self.screen.blit(symbol_user, (userSymbolRightX, userSymbol1Y))

            self.screen.blit(symbol_user, (userSymbolLeftX, userSymbol2Y))
            self.screen.blit(vs, (vsX, vs2Y))
            self.screen.blit(symbol_ai, (userSymbolRightX, userSymbol2Y))

            self.screen.blit(symbol_ai, (userSymbolLeftX, userSymbol3Y))
            self.screen.blit(vs, (vsX, vs3Y))
            self.screen.blit(symbol_ai, (userSymbolRightX, userSymbol3Y))

        if 0 < pregame < 7:
            choose = self.fonts[0].render('Choose AI settings', True, colors['aidiag_dark'])

            if pregame in [1,2]:
                color = self.fonts[1].render("How it's going to play", True, colors['background'])
            if pregame in [3,4]:
                color = self.fonts[1].render('WHITE pieces', True, colors['background'])
            if pregame in [5,6]:
                color = self.fonts[1].render('BLACK pieces', True, colors['background'])


            pg.draw.rect(self.screen, colors['choose_user'], (aiSettingsTextBoxX, aiSettingsTextBoxY, aiSettingsW, aiSettingsTextBoxH))
            self.screen.blit(choose, (aiSettingsTextX, aiSettingsText1Y))
            self.screen.blit(color, (aiSettingsTextX, aiSettingsText2Y))
            if aiSettingsTextBoxX + aiSettingsW - 20 - 5 - 5 < mouse[0] < aiSettingsTextBoxX + aiSettingsW and\
                aiSettingsTextBoxY + aiSettingsTextBoxH - 20 - 5 - 5 < mouse[1] <  aiSettingsTextBoxY + aiSettingsTextBoxH:

                self.screen.blit(symbol_gear_sel, (aiSettingsTextBoxX + aiSettingsW - 20 - 5, aiSettingsTextBoxY + aiSettingsTextBoxH - 20 - 5))
            else:
                self.screen.blit(symbol_gear, (aiSettingsTextBoxX + aiSettingsW - 20 - 5, aiSettingsTextBoxY + aiSettingsTextBoxH - 20 - 5))

        if pregame in [1, 3, 5]:

            pg.draw.rect(self.screen, colors['choose_user'], (aiSettingsBox1X, aiSettingsBox1Y, aiSettingsW, aiSettingsH))
            pg.draw.rect(self.screen, colors['choose_user'], (aiSettingsBox1X, aiSettingsBox2Y, aiSettingsW, aiSettingsH))

            self.screen.blit(symbol_dice, (aiSettingsBox1X+(aiSettingsW-60)//2, aiSettingsBox1Y + +(aiSettingsH-60)//2))
            self.screen.blit(symbol_search, (aiSettingsBox1X+(aiSettingsW-60)//2, aiSettingsBox2Y + +(aiSettingsH-60)//2))

        if pregame in [2, 4, 6]:
            hehe = self.fonts[2].render('aqui hiran los advanced settings', True, colors['aidiag_dark'])
            self.screen.blit(hehe, (aiSettingsBox1X, aiSettingsBox1Y))
        
        if pregame == 7:
            pg.draw.rect(self.screen, colors['choose_black'], (pregameBX, pregameB1Y, pregameButtonWidth, pregameButtonHeight))
            pg.draw.rect(self.screen, colors['choose_random'], (pregameBX, pregameB2Y, pregameButtonWidth, pregameButtonHeight))
            pg.draw.rect(self.screen, colors['choose_white'], (pregameBX, pregameB3Y, pregameButtonWidth, pregameButtonHeight))

            self.screen.blit(b_king, (colorSymbolX, colorSymbol1Y))
            self.screen.blit(symbol_king, (colorSymbolX, colorSymbol2Y))
            self.screen.blit(w_king, (colorSymbolX, colorSymbol3Y))




