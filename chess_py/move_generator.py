
class MoveGenerator:

    def __init__(self) -> None:

        # Bitboard for all moves from each piece in each positions
        # Pawn is separated in black and white
        self.king_moves_map = [0 for x in range(64)]
        self.knight_moves_map = [0 for x in range(64)]
        self.pawn_moves_map = [[0 for x in range(64)], [0 for x in range(64)]]

        # Moves represented as 0-63 (positions on the board)
        self.pawn_moves_indx = [[[] for x in range(64)], [[] for x in range(64)]]
        self.king_moves_indx = [[] for x in range(64)]
        self.knight_moves_indx = [[] for x in range(64)]

        # The number of tiles to the edge going in every direction in every position
        self.tiles_to_edge = [ [[] for x in range(64)] for dirc in range(8)]

        self.dir_offsets = [-8, +1, +8, -1, -7, +9, +7, -9]

        self.precomputeData()

        # Bitbord with all the pinned pieces,
        self.pin_ray_map = 0
        # Map all the pieces that check
        self.check_map = 0
        self.check = False
        self.double_check = False

        # Map with all the accesible tiles for each piece
        self.attack_map = 0
        self.attack_map_no_pawns = 0

        self.pawn_attack_map = 0
        self.knight_attack_map = 0
        self.slider_attack_map = 0

    
    def generateAllMoves(self, board) -> list:
        """Return a list of all possible moves given a board"""

        moves = []
        self.getAttackMaps(board)

        self.generateKingMoves(board, moves)

        if self.double_check:
            return moves

        self.generateSliderMoves(board, moves)
        self.generatePawnMoves(board, moves)
        self.generateKnightMoves(board, moves)

        return moves

    def generateKingMoves(self, board, moves) -> None:
        """Get king moves, included castling"""

        if not board.to_move:
            castling = board.game_state_stack[board.stack_index] >> 6
        else:
            castling = (board.game_state_stack[board.stack_index] >> 4) & 3

        start = board.piece_lists['kings'][board.to_move].occupied_tiles[0]
        
        for target in self.king_moves_indx[start]:
            
            target_piece = board.array[target]
            
            # friend
            if target_piece and target_piece & 8 == (board.to_move << 3):
                continue

            # If move does not put king in check
            if not (1 << target) & self.attack_map:
                moves.append([start, target, 0])


        # CASTLING 
        if not self.check:
            # kingside                                                   
            if castling & 2:
                if not (1 << start + 2) & self.attack_map and not (board.array[start + 1] or board.array[start + 2]) and board.array[start + 3] == (board.to_move << 3 | 4):
                    moves.append([start, start + 2, 5])

            # queenside
            if castling & 1:
                if not (1 << start - 2) & self.attack_map and not (board.array[start - 1] or board.array[start - 2] or board.array[start - 3]) and board.array[start - 4] == (board.to_move << 3 | 4):
                    moves.append([start, start - 2, 6]) 

    def generateSliderMoves(self, board, moves) -> None:
        """Get bishop, rook and queen moves"""

        friend = board.to_move
        opp = board.opponent

        rooks = board.piece_lists['rooks'][friend]
        queens = board.piece_lists['queens'][friend]
        bishops = board.piece_lists['bishops'][friend]

        king_square = board.piece_lists['kings'][friend].occupied_tiles[0]

        self.sliderMoveLoop(board, moves, bishops, 4, 8, king_square, friend, opp)
        self.sliderMoveLoop(board, moves, rooks, 0, 4, king_square, friend, opp)
        self.sliderMoveLoop(board, moves, queens, 0, 8, king_square, friend, opp)

    def sliderMoveLoop(self, board, moves, plist, dstart, dend, king_square, friend, opp):
        """Main loop to get slider piece moves"""

        for i in range(plist.count):

            start = plist.occupied_tiles[i]
            pinned = self.pin_ray_map & (1 << start)

            if self.check and pinned:
                continue

            for direc in range(dstart,dend):

                # if pinned and NOT moving along the ray skip
                if pinned and not self.movingAlongDir(direc, start, king_square):
                    continue

                for n in range(self.tiles_to_edge[direc][start]):

                    target = start + self.dir_offsets[direc] * (n + 1)
                    target_piece = board.array[target]

                    # friend
                    if target_piece and target_piece & 8 == (friend << 3):
                        break

                    stops_check = self.check_map & (1 << target)
                    if not self.check or stops_check:
                        moves.append([start, target, 0])
                    
                    # if opponent or stopping a check stop in that direction
                    if stops_check or target_piece:
                        break
    
    def movingAlongDir(self, direc, start, king_square) -> bool:

        kcol = king_square % 8
        krow = king_square // 8
        scol = start % 8
        srow = start // 8
        
        if direc == 0 or direc == 2: # north-south
            return scol == kcol

        if direc == 1 or direc == 3: # east-west
            return srow == krow

        if direc == 4 or direc == 6: # ne-sw
            return kcol - scol == - (krow - srow)

        if direc == 5 or direc == 7: # nw-se
            return kcol - scol ==  krow - srow

    def generatePawnMoves(self, board, moves) -> None: 

        pawns = board.piece_lists['pawns'][board.to_move]
        ns = 0
        nwse = 7
        nesw = 6

        king_square = board.piece_lists['kings'][board.to_move].occupied_tiles[0]
        # column that just moved 2 foward
        ep_col = ((board.game_state_stack[-1] >> 9) & 15) - 8

        taking_dirs = [5, 6] if board.to_move else [4,7]
        last_pawn_row = 7 if board.to_move else 0
    
        ep_row = 4 if board.to_move else 3
        

        for i in range(pawns.count): 
            
            start = pawns.occupied_tiles[i]

            for i, target in enumerate(self.pawn_moves_indx[board.to_move][start]):

                if board.array[target]:
                    # break instead of continue to avoid jumping from starting file
                    break

                # if pinned and NOT moving along the ray
                if (self.pin_ray_map & (1 << start) and not self.movingAlongDir(ns, start, king_square) )or\
                (self.check and not self.check_map & (1 << target)):
                    continue
                

                # One or two foward                    
                else:
                    # 2
                    if i:
                        moves.append([start, target, 1])
                    else:
                        if target//8 == last_pawn_row:
                            moves.append([start, target, 2, 2])
                            moves.append([start, target, 2, 5])
                        else:
                            moves.append([start, target, 0])
                        

            # taking diagonally
            if start // 8 != last_pawn_row:
                
                if start % 8 != 7: # take to the east

                    target = start + self.dir_offsets[taking_dirs[0]]

                    if not ((self.pin_ray_map & (1 << start) and not self.movingAlongDir(nwse if board.to_move else nesw, start, king_square))or\
                    (self.check and not self.check_map & (1 << target))):

                        piece = board.array[start + self.dir_offsets[taking_dirs[0]]]
                        if piece and piece & 8 == (board.opponent << 3):
                            
                            if target//8 == last_pawn_row:
                                moves.append([start, start + self.dir_offsets[taking_dirs[0]], 2, 2])
                                moves.append([start, start + self.dir_offsets[taking_dirs[0]], 2, 5])
                            else:
                                moves.append([start, start + self.dir_offsets[taking_dirs[0]], 0])


                if start % 8 != 0: # take to the west

                    target = start + self.dir_offsets[taking_dirs[1]]

                    if not ((self.pin_ray_map & (1 << start) and not self.movingAlongDir(nesw if board.to_move else nwse, start, king_square) )or\
                    (self.check and not self.check_map & (1 << target))):

                        piece = board.array[start + self.dir_offsets[taking_dirs[1]]]
                        if piece and piece & 8 == (board.opponent << 3):
                            if target//8 == last_pawn_row:
                                moves.append([start, start + self.dir_offsets[taking_dirs[1]], 2, 2])
                                moves.append([start, start + self.dir_offsets[taking_dirs[1]], 2, 5])
                            else:
                                moves.append([start, start + self.dir_offsets[taking_dirs[1]], 0])



            if ep_col != -8 and start // 8 == ep_row:
                
                if start % 8 + 1 == ep_col:
                    if board.array[start + 1] == (board.opponent << 3) | 1 and\
                        not ((self.pin_ray_map & (1 << start) and not self.movingAlongDir(nwse if board.to_move else nesw, start, king_square) )or\
                        (self.check and not self.check_map & (1 << target))):

                        moves.append([start, start + self.dir_offsets[taking_dirs[0]], 3])
                        
                if start % 8 - 1 == ep_col:
                    if board.array[start - 1] == (board.opponent << 3) | 1 and\
                        not ((self.pin_ray_map & (1 << start) and not self.movingAlongDir(nesw if board.to_move else nwse, start, king_square) )or\
                        (self.check and not self.check_map & (1 << target))):

                        moves.append([start, start + self.dir_offsets[taking_dirs[1]], 4])

    def generateKnightMoves(self, board, moves) -> None:
        
        knights = board.piece_lists['knights'][board.to_move]

        for i in range(knights.count): 
            
            start = knights.occupied_tiles[i]

            # If its pinned it cant move 
            # It doesnt matter if its in check 
            # because it cant take the piece its pinned by
            if self.pin_ray_map & (1 << start):
                continue
            
            for target in self.knight_moves_indx[start]:
                
                target_piece = board.array[target]

                # If piece is same color or
                # In check and is not getting in ray
                if (target_piece and target_piece & 8 == (board.to_move << 3)) or \
                    (self.check and not self.check_map & (1 << target)):
                    continue
                moves.append([start, target, 0])

    def getAttackMaps(self, board) -> None:
        """ Get attack map to validate moves
            Before, I played each move, and if the king was in check that move was not valid
            I doesn't affect normal play, but it slows down the AI search considerably
            
            Attack map includes the position all opp pieces can move to
            Even if it the position is blocked by a piece the same color
            adjusting for taking pieces 
            """

        friend= board.to_move
        opp = board.opponent
        king_tile = board.piece_lists['kings'][friend].occupied_tiles[0]


        start_dir = 0   # north
        end_dir = 8    # nw

        # reset attributes
        self.pin_ray_map = 0
        self.check_map = 0
        self.check = False
        self.double_check = False

        self.pawn_attack_map = 0
        self.knight_attack_map = 0
        self.slider_attack_map = 0

        # Get slider attack map
        for i in range(board.piece_lists['rooks'][opp].count):

            start = board.piece_lists['rooks'][opp].occupied_tiles[i]
            for direc in range(4):

                for n in range(self.tiles_to_edge[direc][start]):
                    target_tile = start + self.dir_offsets[direc] * (n + 1)
                    target_piece = board.array[target_tile]
                    self.slider_attack_map |= (1 << target_tile)
                    if target_tile != king_tile and target_piece:
                        # We also include pieces of the same color
                        # Because those tiles can be under attack if that piece is taken next move
                        break
                        
        for i in range(board.piece_lists['bishops'][opp].count):

            start = board.piece_lists['bishops'][opp].occupied_tiles[i]
            for direc in range(4, 8):

                for n in range(self.tiles_to_edge[direc][start]):
                    target_tile = start + self.dir_offsets[direc] * (n + 1)
                    target_piece = board.array[target_tile]
                    self.slider_attack_map |= (1 << target_tile)
                    if target_tile != king_tile and target_piece:
                        break

        for i in range(board.piece_lists['queens'][opp].count):

            start = board.piece_lists['queens'][opp].occupied_tiles[i]
            for direc in range(8):

                for n in range(self.tiles_to_edge[direc][start]):
                    target_tile = start + self.dir_offsets[direc] * (n + 1)
                    target_piece = board.array[target_tile]
                    self.slider_attack_map |= (1 << target_tile)
                    if target_tile != king_tile and target_piece:
                        break
                    
        # Check if there are sliders
        # To avoid searching 'empty' directions
        if not board.piece_lists['queens'][opp].count: # check opp queens

            if board.piece_lists['rooks'][opp].count: # rooks
                start_dir = 0
            else:
                start_dir = 4

            if board.piece_lists['bishops'][opp].count: # bishops
                end_dir = 8
            else:
                end_dir = 4
        
        # SLIDERS
        for direc in range(start_dir, end_dir):

            friendly_blocking = False
            n = self.tiles_to_edge[direc][king_tile]
            ray_map = 0

            for i in range(n):
                pos_index = king_tile + self.dir_offsets[direc] * (i + 1)
                piece = board.array[pos_index]
                ray_map |= 1 << pos_index

                if piece:# not empty
                    
                    # friend
                    if piece & 8 == (friend << 3):
                        
                        # first friend
                        if not friendly_blocking:
                            friendly_blocking = True
                        # if there is more, there is no pin
                        else:
                            break
                    
                    # foe
                    else:

                        # if diagonal and bishop
                        # or not diagonal and rook
                        # or queen
                        if (direc > 3 and (piece & 7) == 3) or\
                            (direc < 4 and (piece & 7) == 4) or\
                            (piece & 7 == 5): 
                            
                            # Piece is pinned
                            if friendly_blocking:
                                self.pin_ray_map |= ray_map
                                break
                            # Check by slider
                            else:
                                self.check_map |= ray_map
                                self.double_check = self.check
                                self.check = True
                                break

                        # piece cant reach king
                        else:
                            break
                
                else:# empty
                    pass
                pass

        # KNIGHTS
        opp_knights = board.piece_lists['knights'][opp]
        knight_check = False
        for i in range(opp_knights.count):

            attack = self.knight_moves_map[opp_knights.occupied_tiles[i]]
            self.knight_attack_map |= attack

            if not knight_check and (self.knight_attack_map & (1 << king_tile)):
                knight_check = True
                self.double_check = self.check
                self.check = True
                self.check_map |= (1 << opp_knights.occupied_tiles[i])

        
        pawn_directions = [5,6] if board.opponent else [4,7]
        pawn_check = False
        for i in range(board.piece_lists['pawns'][opp].count):

            start = board.piece_lists['pawns'][opp].occupied_tiles[i]
            for direc in pawn_directions:
                
                if self.tiles_to_edge[direc][start]:

                    target_tile = start + self.dir_offsets[direc]


                    target_piece = board.array[target_tile]
                    self.pawn_attack_map |= (1 << target_tile)

                    if not pawn_check and (self.pawn_attack_map & (1 << king_tile)):
                        pawn_check = True
                        self.double_check = self.check
                        self.check = True
                        self.check_map |= (1 << start)



        self.attack_map_no_pawns = self.slider_attack_map | self.knight_attack_map | \
                                   self.king_moves_map[board.piece_lists['kings'][opp].occupied_tiles[0]]
        self.attack_map = self.attack_map_no_pawns | self.pawn_attack_map
        
    def precomputeData(self) -> None:
        
        # KING (w/o castles)
        for square in range(64):
            possible_moves_map = 0
            if square // 8 != 0:
                possible_moves_map |= 1 << (square - 8) # north
                self.king_moves_indx[square].append(square - 8)
                if square % 8 != 0:
                    possible_moves_map |= 1 << (square - 9) # north west
                    self.king_moves_indx[square].append(square - 9)
                if square % 8 != 7:
                    possible_moves_map |= 1 << (square - 7) # north east
                    self.king_moves_indx[square].append(square - 7)

            if square // 8 != 7:
                possible_moves_map |= 1 << (square + 8) # south
                self.king_moves_indx[square].append(square + 8)
                if square % 8 != 0:
                    possible_moves_map |= 1 << (square + 7) # south west
                    self.king_moves_indx[square].append(square + 7)
                if square % 8 != 7:
                    possible_moves_map |= 1 << (square + 9) # south east
                    self.king_moves_indx[square].append(square + 9)

            if square % 8 != 0:
                possible_moves_map |= 1 << (square - 1) # west
                self.king_moves_indx[square].append(square - 1)
            if square % 8 != 7:
                possible_moves_map |= 1 << (square + 1) # east
                self.king_moves_indx[square].append(square + 1)
            
            self.king_moves_map[square] = possible_moves_map

        # KNIGHT
        for square in range(64):

            row = square // 8
            col = square % 8
            possible_moves_map = 0

            if row > 0 and col < 6:
                possible_moves_map |= 1 << (square - 6)
                self.knight_moves_indx[square].append(square - 6)
            if row > 0 and col > 1:
                possible_moves_map |= 1 << (square - 10)
                self.knight_moves_indx[square].append(square - 10)

            if row > 1 and col < 7:
                possible_moves_map |= 1 << (square - 15)
                self.knight_moves_indx[square].append(square - 15)
            if row > 1 and col > 0:
                possible_moves_map |= 1 << (square - 17)
                self.knight_moves_indx[square].append(square - 17)

            if row < 7 and col < 6:
                possible_moves_map |= 1 << (square + 10)
                self.knight_moves_indx[square].append(square + 10)
            if row < 7 and col > 1:
                possible_moves_map |= 1 << (square + 6)
                self.knight_moves_indx[square].append(square + 6)

            if row < 6 and col < 7:
                possible_moves_map |= 1 << (square + 17)
                self.knight_moves_indx[square].append(square + 17)
            if row < 6 and col > 0:
                possible_moves_map |= 1 << (square + 15)
                self.knight_moves_indx[square].append(square + 15)
        
            self.knight_moves_map[square] = possible_moves_map

        # BLACK PAWN (w/o taking and en passant)
        for square in range(64):
            possible_moves_map = 0
            
            if square // 8 != 7:
                possible_moves_map |= 1 << (square + 8)
                self.pawn_moves_indx[1][square].append(square + 8)

            if square // 8 == 1:
                possible_moves_map |= 1 << (square + 16)
                self.pawn_moves_indx[1][square].append(square + 16)

            self.pawn_moves_map[1][square] = possible_moves_map

        # WHITE PAWN (w/o taking and en passant)
        for square in range(64):
            possible_moves_map = 0
            
            if square // 8 != 0:
                possible_moves_map |= 1 << (square - 8)
                self.pawn_moves_indx[0][square].append(square - 8)

            if square // 8 == 6:
                possible_moves_map |= 1 << (square - 16)
                self.pawn_moves_indx[0][square].append(square - 16)

            self.pawn_moves_map[0][square] = possible_moves_map
            
        # TILES TO EDGE IN EACH DIRECCTIONS
        for square in range(64):
            self.tiles_to_edge[0][square] = square // 8                          # n
            self.tiles_to_edge[1][square] = 7 - square % 8                       # e
            self.tiles_to_edge[2][square] = 7 - square // 8                      # s
            self.tiles_to_edge[3][square] = square % 8                           # w

            self.tiles_to_edge[4][square] = min(square // 8, 7 - square % 8)     # ne
            self.tiles_to_edge[5][square] = min(7 - square // 8, 7 - square % 8) # se
            self.tiles_to_edge[6][square] = min(7 - square // 8, square % 8)     # sw
            self.tiles_to_edge[7][square] = min(square // 8, square % 8)         # nw        
