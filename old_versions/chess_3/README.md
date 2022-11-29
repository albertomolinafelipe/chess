# CHESS engine 2.0.0
I want to minimize the things I look up, so the way I encoded the board is probably not the best, or my minimax algorithm is inneficient
The only insipiration I've received is from  Sebastian Lague "Coding Adventure: Chess AI"
Its just a learning experience, once I'm happy with it I'll try to make it as close to SOTA

# to do
Add stalemate, add 100 move draw, add 3 fold draw
Add new select and moved colors


## Encoding the board
    - The board is flatten to rows, from A8 - H8, like playing with white at the bottom
    - Piece encoding
        - Black pieces will be uppercase, white lower
        - Queen q/Q
        - Rook r/R
        - Bishop b/B
        - Knight n/N
        - Pawn p/P, followed by 1 if it has just moved foward to positions or 0 otherwise
        - King k/K
    - The items
        - If the white can castle 0 no, 1 king, 2 queen, 3 both
        - Same with black
        - 100 move rule draw status
        - Players turn 1 black 0 white
        - If someone lost 0 white, 1 black, 2 draw, 3 none

    - To work with the board in the array, the pieces will be encoded as a number
    - A decial number [special][piece][color]
        - Special data
            - Pawn didnt just move two 1
              Not pawn
            - Pawn just moved two 2
        - Piece code
            - Empty 0
            - Pawn 1
            - Bishop 2 
            - Knight 3 
            - Rook 4 
            - Queen 5 
            - King 6 
        - Color
            - White or empty 0
            - Black 1
    
    - Move encoding, 4 numberdigit original row, original col , color code, then target row, target column


class Engine:
    def __init__(self) -> None:
        pass

    def getAllMoves(self, board, look_one_move_foward=True):
        """ Get all possible moves in rewards to board"""
        if board[-2]:
            pawns = [0, 1, 2, 3, 4, 5, 6, 7]
            knights = [8, 9]
            bishops = [10, 11]
            rooks = [12, 13]
            queen = [14]
            king = [15]
            same_color = [0, 15]
            other_color = [16, 32]
            castle = board[-4]
        else:
            pawns = [16, 17, 18, 19, 20, 21, 22, 23]
            knights = [24, 25]
            bishops = [26, 27]
            rooks = [28, 29]
            queen = [30]
            king = [31]
            same_color = [16, 32]
            other_color = [0, 15]
            castle = board[-5]
        moves = []
        for piece_index, piece in enumerate(board):
            if piece: # not empty
                piece_pos = 66 - len(bin(piece))
                # PAWN
                if piece_index in pawns: 

                    if board[-2] and all_positions[piece_pos].s:
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
                        for other_piece in board[:-5]:
                            move_options = move_options | other_piece

                        # No jumping
                        if piece_pos // 8 == 1 and ~move_options == two_foward:
                            move_options = ~0

                        # Filter take options
                        tmp = 0
                        for other in board[0:16]:
                            tmp = tmp | (take_options & other)
                        take_options = tmp

                        # Get positions
                        all_move_options = take_options | ~move_options
                        for pos in all_positions:
                            if pos.bitmap & all_move_options:
                                moves.append([piece_pos, pos.num])
                    elif not board[-2] and all_positions[piece_pos].n: # If it cant move foward, it cant move

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
                        for other_piece in board[:-5]:
                            move_options = move_options | other_piece

                        # No jumping
                        if piece_pos // 8 == 6 and ~move_options == two_foward:
                            move_options = ~0

                        # Filter take options
                        tmp = 0
                        for other in board[0:16]:
                            tmp = tmp | (take_options & other)
                        take_options = tmp

                        # Get positions
                        all_move_options = take_options | ~move_options
                        for pos in all_positions:
                            if pos.bitmap & all_move_options:
                                moves.append([piece_pos, pos.num])
                        
                # KNIGHT
                if piece_index in knights:
                    moves_bitmap = ~knight_move_bitmap[piece_pos]
                    for same in board[same_color[0] : same_color[1]]:
                        moves_bitmap = moves_bitmap | same
                    moves_bitmap = ~moves_bitmap

                    for pos in all_positions:
                        if pos.bitmap & moves_bitmap:
                            moves.append([piece_pos, pos.num])

                # BISHOP AND queen
                if piece_index in bishops or piece_index in queen:

                    ne_moves = 0
                    northeasttile = all_positions[piece_pos].ne
                    cond = True
                    while cond and northeasttile:
                        i = 0
                        while cond and i < 32:
                            intersection = northeasttile.bitmap & board[i]
                            if intersection:
                                if same_color[0] <= i <= same_color[1]:
                                    cond = False
                                if other_color[0] <= i <= other_color[1]:
                                    ne_moves =ne_moves | northeasttile.bitmap
                                    cond = False
                            i += 1
                        if not intersection:
                            ne_moves = ne_moves | northeasttile.bitmap
                        northeasttile = all_positions[northeasttile.num].ne

                    se_moves = 0
                    southeasttile = all_positions[piece_pos].se
                    cond = True
                    while cond and southeasttile:
                        i = 0
                        while cond and i < 32:
                            intersection = southeasttile.bitmap & board[i]
                            if intersection:
                                if same_color[0] <= i <= same_color[1]:
                                    cond = False
                                if other_color[0] <= i <= other_color[1]:
                                    se_moves =se_moves | southeasttile.bitmap
                                    cond = False
                            i += 1
                        if not intersection:
                            se_moves = se_moves | southeasttile.bitmap
                        southeasttile = all_positions[southeasttile.num].se

                    nw_moves = 0
                    northwesttile = all_positions[piece_pos].nw
                    cond = True
                    while cond and northwesttile:
                        i = 0
                        while cond and i < 32:
                            intersection = northwesttile.bitmap & board[i]
                            if intersection:
                                if same_color[0] <= i <= same_color[1]:
                                    cond = False
                                if other_color[0] <= i <= other_color[1]:
                                    nw_moves =nw_moves | northwesttile.bitmap
                                    cond = False
                            i += 1
                        if not intersection:
                            nw_moves = nw_moves | northwesttile.bitmap
                        northwesttile = all_positions[northwesttile.num].nw

                    sw_moves = 0
                    southwesttile = all_positions[piece_pos].sw
                    cond = True
                    while cond and southwesttile:
                        i = 0
                        while cond and i < 32:
                            intersection = southwesttile.bitmap & board[i]
                            if intersection:
                                if same_color[0] <= i <= same_color[1]:
                                    cond = False
                                if other_color[0] <= i <= other_color[1]:
                                    sw_moves =sw_moves | southwesttile.bitmap
                                    cond = False
                            i += 1
                        if not intersection:
                            sw_moves = sw_moves | southwesttile.bitmap
                        southwesttile = all_positions[southwesttile.num].sw

                    
                    all_move_options = (ne_moves | se_moves | nw_moves | sw_moves)
                    for pos in all_positions:
                        if pos.bitmap & all_move_options:
                            moves.append([piece_pos, pos.num])

                # ROOK AND queen
                if piece_index in rooks or piece_index in queen:
                    
                    n_moves = 0
                    northtile = all_positions[piece_pos].n
                    cond = True
                    while cond and northtile:
                        i = 0
                        while cond and i < 32:
                            intersection = northtile.bitmap & board[i]
                            if intersection:
                                if same_color[0] <= i <= same_color[1]:
                                    cond = False
                                if other_color[0] <= i <= other_color[1]:
                                    n_moves =n_moves | northtile.bitmap
                                    cond = False
                            i += 1
                        if not intersection:
                            n_moves = n_moves | northtile.bitmap
                        northtile = all_positions[northtile.num].n

                    s_moves = 0
                    southtile = all_positions[piece_pos].s
                    cond = True
                    while cond and southtile:
                        i = 0
                        while cond and i < 32:
                            intersection = southtile.bitmap & board[i]
                            if intersection:
                                if same_color[0] <= i <= same_color[1]:
                                    cond = False
                                if other_color[0] <= i <= other_color[1]:
                                    s_moves =s_moves | southtile.bitmap
                                    cond = False
                            i += 1
                        if not intersection:
                            s_moves = s_moves | southtile.bitmap
                        southtile = all_positions[southtile.num].s
                    
                    w_moves = 0
                    westtile = all_positions[piece_pos].w
                    cond = True
                    while cond and westtile:
                        i = 0
                        while cond and i < 32:
                            intersection = westtile.bitmap & board[i]
                            if intersection:
                                if same_color[0] <= i <= same_color[1]:
                                    cond = False
                                if other_color[0] <= i <= other_color[1]:
                                    w_moves =w_moves | westtile.bitmap
                                    cond = False
                            i += 1
                        if not intersection:
                            w_moves = w_moves | westtile.bitmap
                        westtile = all_positions[westtile.num].w

                    e_moves = 0
                    eastile = all_positions[piece_pos].e
                    cond = True
                    while cond and eastile:
                        i = 0
                        while cond and i < 32:
                            intersection = eastile.bitmap & board[i]
                            if intersection:
                                if same_color[0] <= i <= same_color[1]:
                                    cond = False
                                if other_color[0] <= i <= other_color[1]:
                                    e_moves =e_moves | eastile.bitmap
                                    cond = False
                            i += 1
                        if not intersection:
                            e_moves = e_moves | eastile.bitmap
                        eastile = all_positions[eastile.num].e

                    

                    all_move_options = (n_moves | s_moves | e_moves | w_moves)
                    for pos in all_positions:
                        if pos.bitmap & all_move_options:
                            moves.append([piece_pos, pos.num])

                # KING
                if piece_index in king:
                    moves_bitmap = ~king_move_bitmap[piece_pos]
                    for same in board[same_color[0] : same_color[1]]:
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
                        for piece in board[:-5]:
                            if right & piece:
                                right_empty = False
                            if right2 & piece:
                                right2_empty = False
                        
                        if right_empty and right2_empty and board[rooks[1]] == all_positions[piece_pos+3].bitmap:
                            moves.append([piece_pos, piece_pos + 2])

                    # Both or just queen
                    if not castle or castle == 2:
                        left = all_positions[piece_pos-1].bitmap
                        left2 = all_positions[piece_pos-2].bitmap
                        left3 = all_positions[piece_pos-3].bitmap
                        left_empty = True
                        left2_empty = True
                        left3_empty = True
                        for piece in board[:-5]:
                            if left & piece:
                                left_empty = False
                            if left2 & piece:
                                left2_empty = False
                            if left3 & piece:
                                left3_empty = False
                        
                        if left_empty and left2_empty and left3_empty and board[rooks[0]] == all_positions[piece_pos-4].bitmap:
                            moves.append([piece_pos, piece_pos - 2])

        if look_one_move_foward:
            good_ones = []
            pass

        return moves

    def getMove(self, board):
        """ Get best move in board"""
        return self.getAllMoves(board)[0]

    def makeMove(self, board, move):
        """ Make move on board """
        pass

    def unmakeMove(self, board, move):
        """ Unmake move on board"""
        pass

