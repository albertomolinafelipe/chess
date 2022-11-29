import numpy as np
import time


king_move_bitmap = [
    4665729213955833856, 11592265440851656704, 5796132720425828352, 2898066360212914176, 1449033180106457088, 724516590053228544, 362258295026614272, 144959613005987840, 13853283560024178688, 16186183351374184448, 8093091675687092224, 4046545837843546112, 2023272918921773056, 1011636459460886528, 505818229730443264, 216739030602088448, 54114388906344448, 63227278716305408, 31613639358152704, 15806819679076352, 7903409839538176, 3951704919769088, 1975852459884544, 846636838289408, 211384331665408, 246981557485568, 123490778742784, 61745389371392, 30872694685696, 15436347342848, 7718173671424, 3307175149568, 825720045568, 964771708928, 482385854464, 241192927232, 120596463616, 60298231808, 30149115904, 12918652928, 3225468928, 3768639488, 1884319744, 942159872, 471079936, 235539968, 117769984, 50463488, 12599488, 14721248, 7360624, 3680312, 1840156, 920078, 460039, 197123, 49216, 57504, 28752, 14376, 7188, 3594, 1797, 770
    ]
knight_move_bitmap = [
    9077567998918656, 4679521487814656, 38368557762871296, 19184278881435648, 9592139440717824, 4796069720358912, 2257297371824128, 1128098930098176, 2305878468463689728, 1152939783987658752, 9799982666336960512, 4899991333168480256, 2449995666584240128, 1224997833292120064, 576469569871282176, 288234782788157440, 4620693356194824192, 11533718717099671552, 5802888705324613632, 2901444352662306816, 1450722176331153408, 725361088165576704, 362539804446949376, 145241105196122112, 18049583422636032, 45053588738670592, 22667534005174272, 11333767002587136, 5666883501293568, 2833441750646784, 1416171111120896, 567348067172352, 70506185244672, 175990581010432, 88545054707712, 44272527353856, 22136263676928, 11068131838464, 5531918402816, 2216203387392, 275414786112, 687463207072, 345879119952, 172939559976, 86469779988, 43234889994, 21609056261, 8657044482, 1075839008, 2685403152, 1351090312, 675545156, 337772578, 168886289, 84410376, 33816580, 4202496, 10489856, 5277696, 2638848, 1319424, 659712, 329728, 132096
]

class Position:
    def __init__(self, num):
        self.num = num
        self.bitmap = 2 ** (63 - num)
        self.n = 0
        self.s = 0
        self.w = 0
        self.e = 0
        self.nw = 0
        self.ne = 0
        self.sw = 0
        self.se = 0
all_positions = [Position(x) for x in range(64)]
# Create position graph
for i, position in enumerate(all_positions):
    # North
    if i // 8 > 0:
        position.n = all_positions[i - 8]
    # South
    if i // 8 < 7:
        position.s = all_positions[i + 8]
    # East
    if i % 8 < 7:
        position.e = all_positions[i + 1]
    # West
    if i % 8 > 0:
        position.w = all_positions[i - 1]
    # North east
    if i // 8 > 0 and i % 8 < 7:
        position.ne = all_positions[i - 7]
    # North west
    if i // 8 > 0 and i % 8 > 0:
        position.nw = all_positions[i - 9]
    # South east
    if i // 8 < 7 and i % 8 < 7:
        position.se = all_positions[i + 9]
    # South west
    if i // 8 != 7 and i % 8 != 0:
        position.sw = all_positions[i + 7]

class Engine:
    def __init__(self, strategy) -> None:
        self.positions_checked = 0
        self.depth = strategy[0]
        self.abp = strategy[1]
        self.move_ordering = strategy[2]

    def getAllMoves(self, board, look_one_move_foward=True):
        start = time.time()
        turn = board[-1][-2]
        pawns = 0
        knights = 1
        bishops = 2
        rooks = 3
        queens = 4
        king = 5
        if turn:  
            same_color = [0, 6]
            other_color = [6, 12]
            rook_index = 3
            castle = board[-1][-4]
        else:
            same_color = [6, 12]
            other_color = [0, 6]
            rook_index = 9
            castle = board[-1][-5]

        moves = []
        for piece_index, piece_group in enumerate(board[same_color[0]: same_color[1]]):
            for piece in piece_group:
                if piece:
                    piece_pos = 66 - len(bin(piece))
                    if piece_index == pawns:
                        if turn and all_positions[piece_pos].s:
                            # Add move options
                            move_options = all_positions[piece_pos].s.bitmap
                            if piece_pos // 8 == 1:
                                two_foward = all_positions[all_positions[piece_pos].s.num].s.bitmap
                            else:
                                two_foward = 0
                            move_options = ~(move_options | two_foward)

                            # Add take options
                            take_options = 0
                            if all_positions[piece_pos].sw:
                                take_options = take_options | all_positions[piece_pos].sw.bitmap
                            if all_positions[piece_pos].se:
                                take_options = take_options | all_positions[piece_pos].se.bitmap
                            
                            # Filter move options
                            for group in board[:-1]:
                                for other_piece in group:
                                    move_options = move_options | other_piece

                            # No jumping
                            if piece_pos // 8 == 1 and ~move_options == two_foward:
                                move_options = ~0

                            # Filter take options
                            tmp = 0
                            for group in board[6:12]:
                                for other_piece in group:
                                    tmp = tmp | (take_options & other_piece)
                            take_options = tmp

                            # Get positions
                            all_move_options = take_options | ~move_options
                            for pos in all_positions:
                                if pos.bitmap & all_move_options:
                                    moves.append([piece_pos, pos.num])

                        elif not turn and all_positions[piece_pos].n:
                            # Add move options
                            move_options = all_positions[piece_pos].n.bitmap
                            if piece_pos // 8 == 6:
                                two_foward = all_positions[all_positions[piece_pos].n.num].n.bitmap
                            else:
                                two_foward = 0
                            move_options = ~(move_options | two_foward)

                            # Add take options
                            take_options = 0
                            if all_positions[piece_pos].nw:
                                take_options = take_options | all_positions[piece_pos].nw.bitmap
                            if all_positions[piece_pos].ne:
                                take_options = take_options | all_positions[piece_pos].ne.bitmap
                            
                            # Filter move options
                            for group in board[:-1]:
                                for other_piece in group:
                                    move_options = move_options | other_piece

                            # No jumping
                            if piece_pos // 8 == 6 and ~move_options == two_foward:
                                move_options = ~0

                            tmp = 0
                            for group in board[0:6]:
                                for other_piece in group:
                                    tmp = tmp | (take_options & other_piece)
                            take_options = tmp

                            # Get positions
                            all_move_options = take_options | ~move_options
                            for pos in all_positions:
                                if pos.bitmap & all_move_options:
                                    moves.append([piece_pos, pos.num])

                    if piece_index == knights:
                        moves_bitmap = ~knight_move_bitmap[piece_pos]
                        for group_same_color in board[same_color[0] : same_color[1]]:
                            for same in group_same_color:
                                moves_bitmap = moves_bitmap | same
                        moves_bitmap = ~moves_bitmap

                        for pos in all_positions:
                            if pos.bitmap & moves_bitmap:
                                moves.append([piece_pos, pos.num])
                    
                    if piece_index == bishops or piece_index == queens:
                        ne_moves = 0
                        northeasttile = all_positions[piece_pos].ne
                        cond = True
                        while cond and northeasttile:
                            i = 0
                            while cond and i < 12:
                                p = 0
                                while cond and p < len(board[i]):
                                    intersection = northeasttile.bitmap & board[i][p]
                                    if intersection:
                                        if same_color[0] <= i < same_color[1]:
                                            cond = False
                                        if other_color[0] <= i < other_color[1]:
                                            ne_moves =ne_moves | northeasttile.bitmap
                                            cond = False
                                    p += 1
                                i += 1
                            if not intersection:
                                ne_moves = ne_moves | northeasttile.bitmap
                            northeasttile = all_positions[northeasttile.num].ne


                        nw_moves = 0
                        northwesttile = all_positions[piece_pos].nw
                        cond = True
                        while cond and northwesttile:
                            i = 0
                            while cond and i < 12:
                                p = 0
                                while cond and p < len(board[i]):
                                    intersection = northwesttile.bitmap & board[i][p]
                                    if intersection:
                                        if same_color[0] <= i < same_color[1]:
                                            cond = False
                                        if other_color[0] <= i < other_color[1]:
                                            nw_moves =nw_moves | northwesttile.bitmap
                                            cond = False
                                    p += 1
                                i += 1
                            if not intersection:
                                nw_moves = nw_moves | northwesttile.bitmap
                            northwesttile = all_positions[northwesttile.num].nw

                        se_moves = 0
                        southeasttile = all_positions[piece_pos].se
                        cond = True
                        while cond and southeasttile:
                            i = 0
                            while cond and i < 12:
                                p = 0
                                while cond and p < len(board[i]):
                                    intersection = southeasttile.bitmap & board[i][p]
                                    if intersection:
                                        if same_color[0] <= i < same_color[1]:
                                            cond = False
                                        if other_color[0] <= i < other_color[1]:
                                            se_moves =se_moves | southeasttile.bitmap
                                            cond = False
                                    p += 1
                                i += 1
                            if not intersection:
                                se_moves = se_moves | southeasttile.bitmap
                            southeasttile = all_positions[southeasttile.num].se


                        sw_moves = 0
                        southwesttile = all_positions[piece_pos].sw
                        cond = True
                        while cond and southwesttile:
                            i = 0
                            while cond and i < 12:
                                p = 0
                                while cond and p < len(board[i]):
                                    intersection = southwesttile.bitmap & board[i][p]
                                    if intersection:
                                        if same_color[0] <= i < same_color[1]:
                                            cond = False
                                        if other_color[0] <= i < other_color[1]:
                                            sw_moves =sw_moves | southwesttile.bitmap
                                            cond = False
                                    p += 1
                                i += 1
                            if not intersection:
                                sw_moves = sw_moves | southwesttile.bitmap
                            southwesttile = all_positions[southwesttile.num].sw

                        
                        all_move_options = (ne_moves | se_moves | nw_moves | sw_moves)
                        for pos in all_positions:
                            if pos.bitmap & all_move_options:
                                moves.append([piece_pos, pos.num])
                    
                    if piece_index == rooks or piece_index == queens:
                        n_moves = 0
                        northtile = all_positions[piece_pos].n
                        cond = True
                        while cond and northtile:
                            i = 0
                            while cond and i < 12:
                                p = 0
                                while cond and p < len(board[i]):
                                    intersection = northtile.bitmap & board[i][p]
                                    if intersection:
                                        if same_color[0] <= i < same_color[1]:
                                            cond = False
                                        if other_color[0] <= i < other_color[1]:
                                            n_moves =n_moves | northtile.bitmap
                                            cond = False
                                    p += 1
                                i += 1
                            if not intersection:
                                n_moves = n_moves | northtile.bitmap
                            northtile = all_positions[northtile.num].n

                        s_moves = 0
                        southtile = all_positions[piece_pos].s
                        cond = True
                        while cond and southtile:
                            i = 0
                            while cond and i < 12:
                                p = 0
                                while cond and p < len(board[i]):
                                    intersection = southtile.bitmap & board[i][p]
                                    if intersection:
                                        if same_color[0] <= i < same_color[1]:
                                            cond = False
                                        if other_color[0] <= i < other_color[1]:
                                            s_moves =s_moves | southtile.bitmap
                                            cond = False
                                    p += 1
                                i += 1
                            if not intersection:
                                s_moves = s_moves | southtile.bitmap
                            southtile = all_positions[southtile.num].s
                        
                        w_moves = 0
                        westtile = all_positions[piece_pos].w
                        cond = True
                        while cond and westtile:
                            i = 0
                            while cond and i < 12:
                                p = 0
                                while cond and p < len(board[i]):
                                    intersection = westtile.bitmap & board[i][p]
                                    if intersection:
                                        if same_color[0] <= i < same_color[1]:
                                            cond = False
                                        if other_color[0] <= i < other_color[1]:
                                            w_moves =w_moves | westtile.bitmap
                                            cond = False
                                    p += 1
                                i += 1
                            if not intersection:
                                w_moves = w_moves | westtile.bitmap
                            westtile = all_positions[westtile.num].w

                        e_moves = 0
                        eastile = all_positions[piece_pos].e
                        cond = True
                        while cond and eastile:
                            i = 0
                            while cond and i < 12:
                                p = 0
                                while cond and p < len(board[i]):
                                    intersection = eastile.bitmap & board[i][p]
                                    if intersection:
                                        if same_color[0] <= i < same_color[1]:
                                            cond = False
                                        if other_color[0] <= i < other_color[1]:
                                            e_moves =e_moves | eastile.bitmap
                                            cond = False
                                    p += 1
                                i += 1
                            if not intersection:
                                e_moves = e_moves | eastile.bitmap
                            eastile = all_positions[eastile.num].e

                        

                        all_move_options = (n_moves | s_moves | e_moves | w_moves)
                        for pos in all_positions:
                            if pos.bitmap & all_move_options:
                                moves.append([piece_pos, pos.num])
                    
                    if piece_index == king:
                        moves_bitmap = ~king_move_bitmap[piece_pos]
                        for group_same_color in board[same_color[0] : same_color[1]]:
                            for same in group_same_color:
                                moves_bitmap = moves_bitmap | same
                        moves_bitmap = ~moves_bitmap

                        for pos in all_positions:
                            if pos.bitmap & moves_bitmap:
                                moves.append([piece_pos, pos.num])

                        # Both or just king
                        if castle < 2:
                            
                            right = all_positions[piece_pos+1].bitmap
                            right2 = all_positions[piece_pos+2].bitmap
                            right_empty = True
                            right2_empty = True

                            for group in board[:-1]:
                                for other in group:
                                    if right & other:
                                        right_empty = False
                                    if right2 & other:
                                        right2_empty = False


                            if right_empty and right2_empty and board[rook_index][1] == all_positions[piece_pos+3].bitmap:
                                moves.append([piece_pos, piece_pos + 2])

                        # Both or just queen
                        if not castle or castle == 2:
                            left = all_positions[piece_pos-1].bitmap
                            left2 = all_positions[piece_pos-2].bitmap
                            left3 = all_positions[piece_pos-3].bitmap
                            left_empty = True
                            left2_empty = True
                            left3_empty = True
                            for group in board[:-1]:
                                for other in group:
                                    if left & other:
                                        left_empty = False
                                    if left2 & other:
                                        left2_empty = False
                                    if left3 & other:
                                        left3_empty = False
                            
                            if left_empty and left2_empty and left3_empty and board[rook_index][0] == all_positions[piece_pos-4].bitmap:
                                moves.append([piece_pos, piece_pos - 2])
        

        if look_one_move_foward:
            good_ones = []
            board[-1][-2] = not board[-1][-2]
            check = self.lookForCheck(board)
            board[-1][-2] = not board[-1][-2]
            
            for move in moves:
                info = self.makeMove(board, move)
                if not self.lookForCheck(board):
                    good_ones.append(move)
                self.unmakeMove(board, move, info)
            
            if check and not len(good_ones): # checkmate
                board[-1][-1] = board[-1][-2]

            if not check and not len(good_ones): # stalemate
                board[-1][-1] = 2
            if board[-1][-3] > 100:
                board[-1][-1] = 2
            moves = good_ones.copy()

        
        return moves

    def getMove(self, board, all_moves):
        """ Get best move in board"""
        self.positions_checked = 0
        best_move = None

        if self.move_ordering:
                self.orderMoves(all_moves, board)

        if self.abp: # alpha beta prunning            
            beta = np.inf
            alpha = -np.inf
            for move in all_moves:
                info = self.makeMove(board, move)
                evaluation = - self.searchABP(board, self.evaluate_v1, 
                                              self.depth-1, -beta, -alpha)
                self.unmakeMove(board, move, info)
                if evaluation >= beta:
                    return move
                    #beta = evaluation
                if evaluation > alpha:
                    best_move = move
                
                alpha = max(alpha, evaluation)
            
        else: # seaching w/o abp
            best_eval = -np.inf
            for move in all_moves:
                info = self.makeMove(board, move)
                evaluation = - self.search(board, self.evaluate_v1, self.depth-1)
                self.unmakeMove(board, move, info)
                if evaluation > best_eval:
                    best_eval = evaluation
                    best_move = move
        return best_move

    def makeMove(self, board, move):
        """ Make move on board """
        # more_info = 
        # [piece_group(if a piece was taken), 
        # position in piece_group, 

        # if it was a pawn promotion,
        # if it was a castle move,

        # what castle was before the move,
        # what draw move rule count was]

        if board[-1][-2]:
            promotion = 7
            pawn_index = 0
            rook_index = 3
            queen_index = 4
            king_index = 5
            king_pos = 4
            castle = -4
        else:
            promotion = 0
            pawn_index = 6
            rook_index = 9
            queen_index = 10
            king_index = 11
            king_pos = 60
            castle = -5
        
        pawn_move = False
        weird_case = False # for castles and promotions
        more_info = [None, None, False, False, board[-1][castle], board[-1][-3]]

        for piece_index, piece_group in enumerate(board[:-1]):
            for i, piece in enumerate(piece_group):
                if piece == all_positions[move[0]].bitmap:
                    if piece_index == rook_index:
                        more_info[3] = board[-1][castle]

                        if move[0] % 8 == 7 and not castle:
                            board[-1][castle] = 2 # only queenside
                        if move[0] % 8 == 7 and castle == 1: 
                            board[-1][castle] = 3 # cant castle anymore
                        if move[0] % 8 == 0 and not castle:
                            board[-1][castle] = 1 # only kingiside
                        if move[0] % 8 == 0 and castle == 2:
                            board[-1][castle] = 3 # cant castle anymore
                        board[piece_index][i] = all_positions[move[1]].bitmap

                    elif piece_index == pawn_index:
                        pawn_move = True
                        if move[1] // 8 == promotion:
                            weird_case = True
                            board[piece_index].pop(i)
                            board[queen_index].append(all_positions[move[1]].bitmap)
                            more_info[2] = True
                        else:
                            board[piece_index][i]= all_positions[move[1]].bitmap

                    elif piece_index == king_index:
                        more_info[4] = board[-1][castle]
                        board[-1][castle] = 3 # cant castle anymore

                        # Castling
                        if move[0] == king_pos and move[1] == king_pos + 2:
                            weird_case = True
                            board[piece_index][i]= all_positions[move[1]].bitmap
                            board[rook_index][1] = all_positions[move[1] - 1].bitmap
                            more_info[3] = True
                        elif move[0] == king_pos and move[1] == king_pos - 2:
                            weird_case = True
                            board[piece_index][i]= all_positions[move[1]].bitmap
                            board[rook_index][0] = all_positions[move[1] + 1].bitmap
                            more_info[3] = True
                        else:
                            board[piece_index][i]= all_positions[move[1]].bitmap

                    # Everyother piece
                    else:
                        board[piece_index][i]= all_positions[move[1]].bitmap
                        board[-1][castle] = 3 # cant castle anymore

                # Piece taken
                elif not weird_case and piece == all_positions[move[1]].bitmap:
                    more_info[0] = piece_index
                    more_info[1] = i
                    board[piece_index][i] = 0
        
        # change turn
        board[-1][-2] = not board[-1][-2]

        # change moves w/o pawn or piece_taken
        if not (more_info[0] is not None or pawn_move):
            board[-1][-3] += 1
        else:
            board[-1][-3] = 0

        return more_info

    def unmakeMove(self, board, move, info):
        """ Unmake move on board"""

        if board[-1][-2]:
            castle = -5
            pawn_index = 6
        else:
            pawn_index = 0
            castle = -4

        if not info[2]:
            for piece_index, piece_group in enumerate(board[:-1]):
                for i, piece in enumerate(piece_group):
                    if piece == all_positions[move[1]].bitmap:
                        if piece_index == pawn_index + 5 and info[3]: # king castle
                            if move[1] % 8 == 6: # kingside castle
                                board[piece_index][i] = all_positions[move[0]].bitmap
                                board[pawn_index + 3][1] = all_positions[move[0]+3].bitmap
                            elif move[1] % 8 == 2: # queenside castle
                                board[piece_index][i] = all_positions[move[0]].bitmap
                                board[pawn_index + 3][0] = all_positions[move[0]-4].bitmap
                        else:
                            board[piece_index][i] = all_positions[move[0]].bitmap

        if info[2]: # pawn promotion
            board[pawn_index].append(all_positions[move[0]].bitmap)
            board[pawn_index + 4] = board[pawn_index + 4][:-1] # take away added queen

        if info[0] is not None: # piece was taken
            board[info[0]][info[1]] = all_positions[move[1]].bitmap

        board[-1][-3] = info[-1]
        board[-1][castle] = info[-2]
        board[-1][-2] = not board[-1][-2]
        board[-1][-1] = 3

    def lookForCheck(self, board):
        """ Returns if the player that moves now can check the others king """
        if board[-1][-2]:
            king_pos = 66 - len(bin(board[11][0]))
        else:
            king_pos = 66 - len(bin(board[5][0]))

        all_moves = self.getAllMoves(board, look_one_move_foward=False)
        for move in all_moves:
            if move[1] == king_pos:
                return True
        return False

    def search(self, board, func, depth):
        best_eval = - np.inf
        if not depth:
            self.positions_checked += 1
            return func(board)

        all_moves = self.getAllMoves(board)

        if not len(all_moves):
            if self.lookForCheck(board):
                return -np.inf
            else:
                return 0
        
        for move in all_moves:
            info = self.makeMove(board, move)
            evaluation = - self.search(board, func, depth-1)
            self.unmakeMove(board, move, info)
            best_eval = max(best_eval, evaluation)

        return best_eval

    def searchABP(self, board, func, depth, alpha, beta):
        if not depth:
            self.positions_checked += 1
            return func(board)

        all_moves = self.getAllMoves(board)

        if not len(all_moves):
            if self.lookForCheck(board):
                return -np.inf
            else:
                return 0
        
        for move in all_moves:
            info = self.makeMove(board, move)
            evaluation = - self.searchABP(board, func, depth-1, -beta, -alpha)
            self.unmakeMove(board, move, info)
            if evaluation >= beta:
                return beta
            alpha = max(alpha, evaluation)
            
        return alpha

    def evaluate_v1(self, board):
        if board[-1][-2]:
            piece_values = [1, 3, 3, 5, 9, 0, -1, -3, -3, -5, -9, 0]
        else:
            piece_values = [-1, -3, -3, -5, -9, 0, 1, 3, 3, 5, 9, 0]            
        val = 0
        for piece_index, piece_group in enumerate(board[:-1]):
            for piece in piece_group:
                if piece:
                    val += piece_values[piece_index]
        return val

    def orderMoves(self, all_moves, board):
        pass