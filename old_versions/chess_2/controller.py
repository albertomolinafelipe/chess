import numpy as np

# <special data><piece code><color>
codes = {
    'p0': '110',
    'p1': '210',
    'P0': '111',
    'P1': '211',
    'k': '160',
    'K': '161',
    'q': '150',
    'Q': '151',
    'n': '130',
    'N': '131',
    'r': '140',
    'R': '141',
    'b': '120',
    'B': '121',
    '0': '3'
}

class Controller:
    def __init__(self):
        pass
    def numberToCoordinate(self, pos):
        """ Number(0-99) in 10x10 grid to row,col in 8x8 inside it"""
        return str(((pos-11-2*(pos // 10 - 1)) // 8)) + str(((pos-11-2*(pos // 10 - 1)) % 8))

    def coordinateToNumber(self, row_col):
        """Coordinates in 8x8 to number (0-63)"""
        return int(row_col[0]) * 8 + int(row_col[1])

    def checkTile(self, cell, turn):
        """
        0 empty
        1 other color
        2 same color
        3 white space
        """
        if cell == '3':
            return 0
        elif cell == '4':
            return 3
        elif cell[-1] != turn:
            return 1
        elif cell[-1] == turn:
            return 2

    def move(self, board, org, target, promotion=False, turn=None, two=False):
        """ True if a piece was taken"""

        taken = False
        if board[target] != '3':
            taken = True
        # pawn moving 2
        if two:
            board[target] = '2' + board[org][-2:]
        
        # PRomoting pawn to queen
        elif promotion:
            if turn == '0':
                board[target] = codes['q']
            else:
                board[target] = codes['Q']

        # Pawn diagonal
        elif board[org][-2] == '1' and org % 8 != target % 8:
            if org // 8 < target // 8 and board[target-8][:-1] == '21':
                board[target-8] = '3'
            elif org // 8 > target // 8 and board[target+8][:-1] == '21':
                board[target+8] = '3'
            board[target] = board[org]
            taken = True
        else:
            board[target] = board[org]
        board[org] = '3'
        return taken

    def codeBoard(self, board):
        for i, cell in enumerate(board):
            if i < 64:
                board[i] = codes[cell]

        return board

    def makeMove(self, move, board):
        turn = board[-2]
        draw = str(int(board[-3]) + 1)
        if turn == '0':
            castle = board[-5]
        else:
            castle = board[-4]

        org = self.coordinateToNumber(move[:-2])
        target = self.coordinateToNumber(move[-2:])

        # PAWN
        if board[org][-2] == '1':
            if turn == '0':
                end_row = 0
                passant_row = 4
            else:
                end_row = 7
                passant_row = 3
            if (target // 8) == end_row:
                self.move(board, org, target, promotion=True, turn=turn)
            elif (target // 8) == passant_row:
                self.move(board, org, target, promotion=True, turn=turn, two=True)
            else:
                self.move(board, org, target)
            draw = '0'

        # ROOK
        elif board[org][-2] == '4':
            take = self.move(board, org, target)
            if take:
                draw = '0'
            if org % 8 == 7 and castle == '3':
                castle = '2'
            if org % 8 == 7 and castle == '1':
                castle = '0'
            if org % 8 == 0 and castle == '3':
                castle = '1'
            if org % 8 == 0 and castle == '2':
                castle = '0'

        # KING
        elif board[org][-2] == '6':
            if turn == '0':
                k_row = 7
            else:
                k_row = 0
            # king side castle
            if (org // 8) == k_row and (target // 8) == k_row and (org % 8) == 4 and (target % 8) == 6:
                self.move(board, org, target)
                self.move(board, org + 3, org + 1) # rook
                castle = '0'
            # queen side castle
            elif (org // 8) == k_row and (target // 8) == k_row and (org % 8) == 4 and (target % 8) == 2:
                self.move(board, org, target)
                self.move(board, org - 4, org - 1) # rook
                castle = '0'
            else:
                take = self.move(board, org, target)
                if take:
                    draw = '0'
                castle = '0'

        # QUEEN, BISHOP, KNIGHT
        else:
            take = self.move(board, org, target)
            if take:
                draw = '0'


        # TURN
        if turn == '0':
            board[-2] = '1'
            k_row = 7
            board[-5] = castle
        else:
            board[-2] = '0'
            k_row = 0
            board[-4] = castle

        # DRAW RULE
        board[-3] = draw
        return board

    def getMoves(self, board_and_info, recursive=True):
        
        board = board_and_info[:-5]
        info = board_and_info[-5:]

        turn = info[-2]
        if turn == '0':
            castle = info[-5]
        else:
            castle = info[-4]
        
        # Adding whitespace
        for i in range(63, -1, -1):
            if i % 8 == 7:
                board = np.insert(board, i+1,'4')
            if i % 8 == 0:
                board = np.insert(board, i,'4')
        board = np.concatenate((['4']*10, board))
        board = np.concatenate((board, ['4']*10))

        moves = []
        for i, cell in enumerate(board):
            if cell != '3' and cell != '4' and cell[-1] == turn:
                # PAWNS
                if cell[-2] == '1':
                    if cell[-1] == '0':
                        # white pawn moves up 
                        dirc = -1
                        start = '6'
                    else:
                        # black moves down
                        dirc = 1
                        start = '1'
                    
                    # One foward
                    if not self.checkTile(board[i + 10 * dirc], turn): 
                        moves.append(self.numberToCoordinate(i) + self.numberToCoordinate(i + 10 * dirc))
                    # Two foward
                    if self.numberToCoordinate(i)[0] == start and not self.checkTile(board[i + 10 * dirc], turn) and not self.checkTile(board[i + 20 * dirc], turn):
                        moves.append(self.numberToCoordinate(i) + self.numberToCoordinate(i + 20 * dirc))

                    # Taking diagonally
                    # En passant
                    if 0 <= i + 11 * dirc < 100 and\
                        (self.checkTile(board[i + 11 * dirc], turn) == 1 or\
                        (not self.checkTile(board[i + 11 * dirc], turn) and self.checkTile(board[i + dirc], turn) == 1 and board[i + dirc][:-1] == '21')):
                            moves.append(self.numberToCoordinate(i) + self.numberToCoordinate(i + 11 * dirc))
                    
                    if 0 <= i + 9 * dirc < 100 and\
                        (self.checkTile(board[i + 9 * dirc], turn) == 1 or\
                        (not self.checkTile(board[i + 9 * dirc], turn) and self.checkTile(board[i - dirc], turn) == 1 and board[i - dirc][:-1] == '21')):
                            moves.append(self.numberToCoordinate(i) + self.numberToCoordinate(i + 9 * dirc))

                # BISHOP 
                if cell[-2] == '2':
                    for dirc in [-11, 11, -9, 9]:
                        cond = True
                        cnt = 1
                        while cond:
                            checkTile = self.checkTile(board[i + dirc * cnt], turn)
                            if 2 <= checkTile <= 3:
                                cond = False
                            elif checkTile < 2:
                                moves.append(self.numberToCoordinate(i) + self.numberToCoordinate(i + dirc * cnt))
                                if checkTile == 1:
                                    cond = False
                            cnt += 1
                
                # KNIGHT
                if cell[-2] == '3':
                    # Im going to sort of hard code it sorry
                    options = [8, 12, 21, 19]
                    for op in options:
                        for sig in [-1, 1]:
                            if 0 <= i + op*sig < 100 and self.checkTile(board[i+op*sig], turn) < 2:
                                if  (op == 12 and\
                                    (self.checkTile(board[i+2*sig], turn) < 3 and self.checkTile(board[i+1*sig], turn) < 3) or (self.checkTile(board[i+10*sig], turn) < 3 and self.checkTile(board[i+11*sig], turn) < 3)) or\
                                    (op == 8 and\
                                    (self.checkTile(board[i-2*sig], turn) < 3 and self.checkTile(board[i-1*sig], turn) < 3) or (self.checkTile(board[i+10*sig], turn) < 3 and self.checkTile(board[i+9*sig], turn) < 3)) or\
                                    (op == 19 and\
                                    (self.checkTile(board[i+9*sig], turn) < 3 and self.checkTile(board[i-1*sig], turn) < 3) or (self.checkTile(board[i+20*sig], turn) < 3 and self.checkTile(board[i+10*sig], turn) < 3)) or\
                                    (op == 21 and\
                                    (self.checkTile(board[i+1*sig], turn) < 3 and self.checkTile(board[i+11*sig], turn) < 3) or (self.checkTile(board[i+10*sig], turn) < 3 and self.checkTile(board[i+20*sig], turn) < 3)):
                                        moves.append(self.numberToCoordinate(i) + self.numberToCoordinate(i + op*sig))

                # ROOK
                if cell[-2] == '4':
                    for dirc in [-1, 1, 10, -10]:
                        cond = True
                        cnt = 1
                        while cond:
                            checkTile = self.checkTile(board[i + dirc * cnt], turn)
                            if 2 <= checkTile <= 3:
                                cond = False
                            else:
                                moves.append(self.numberToCoordinate(i) + self.numberToCoordinate(i + dirc * cnt))
                                if checkTile == 1:
                                    cond = False
                            cnt += 1
                            
                # QUEEN
                if cell[-2] == '5':
                    for dirc in [-1, 1, 10, -10, -11, 11, -9, 9]:
                        cond = True
                        cnt = 1
                        while cond:
                            checkTile = self.checkTile(board[i + dirc * cnt], turn)
                            if 2 <= checkTile <= 3:
                                cond = False
                            elif checkTile < 2:
                                moves.append(self.numberToCoordinate(i) + self.numberToCoordinate(i + dirc * cnt))
                                if checkTile == 1:
                                    cond = False
                            cnt += 1
                
                # KING
                if cell[-2] == '6':
                    for move in [1, 9, 10, 11, -1, -9, -10, -11]:
                            if self.checkTile(board[i + move], turn) < 2:
                                moves.append(self.numberToCoordinate(i) + self.numberToCoordinate(i + move))
                    # king side castle
                    if (castle == '1' or castle == '3') and board[i+1] == '0' and board[i+2] == '0' and board[i+3][-2:] == '4'+ cell[-1]:
                        moves.append(self.numberToCoordinate(i) + self.numberToCoordinate(i + 2))
                    # queen side castle
                    if castle == '2' or castle == '3' and board[i-1] == '0' and board[i-2] == '0' and board[i-3] == '0'and board[i-4][-2:] == '4'+ cell[-1]:
                        moves.append(self.numberToCoordinate(i) + self.numberToCoordinate(i - 2))
        
        if recursive:
            good_ones = []
            for move in moves:
                if not self.lookForCheck(self.makeMove(move, np.copy(board_and_info))):
                    good_ones.append(move)
            moves = good_ones.copy()
        return moves
    
    def lookForCheck(self, original):
        """ Look for check on player.color = turn"""
        turn = original[-2]
        board = np.copy(original)
        if turn == '0':
            op = '1'
            king = codes['k']
        else:
            op = '0'
            king = codes['K']

        for i, piece in enumerate(board[:-5]):
            if piece == king:
                pos_king = i
        check = False
        board[-2] = op
        moves = self.getMoves(board, recursive=False)
        for move in moves:
            if self.coordinateToNumber(move[-2:]) == pos_king:
                check = True
        return check

    def changeResult(self, board):
        moves = self.getMoves(board)
        turn = board[-2]
        check = self.lookForCheck(board)
        # checkmate, turn loses
        if check and len(moves) == 0:
            board[-1] = turn
        # stalemate
        # 100 draw rule
        elif (not check and len(moves) == 0) or\
            (int(board[-3]) > 100):
            board[-1] = '2'
