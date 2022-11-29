from move_generator import MoveGenerator
from piece_list import PieceList

"""
Piece codes
1 pawn
2 knight
3 bishop
4 rook
5 queen
6 king
+ 8 if black piece
"""
piece_codes = ['pawns', 'knights', 'bishops', 'rooks', 'queens', 'kings']

class Board:

    def __init__(self) -> None:

        self.move_gen = MoveGenerator()

        # Piece code for 64 tiles
        # color | type, type starts at 1, 0 means empty
        self.array = [0 for x in range(64)]
        self.piece_lists = {
            'pawns': [PieceList(8), PieceList(8)],
            'knights': [PieceList(10), PieceList(10)],
            'bishops': [PieceList(2), PieceList(2)],
            'rooks': [PieceList(2), PieceList(2)],
            'queens': [PieceList(10), PieceList(10)],
            'kings':[PieceList(1), PieceList(1)]
        }

        self.piece_codes = [None, 'pawns', 'knights', 'bishops', 'rooks', 'queens', 'kings']

        self.to_move = None # 0 white, 1 black
        self.opponent = None

        # captured piece                    0-2 bit piece 3 bit color
        # castling legalities               4-7 bit, 4-5 white, 6-7 black
        # column that can be en passant-ed  8-11 bit, first bit 1 from the left if there is any, other 3 count up to 8
        # draw move counter                 12-
        self.stack_index = 0
        self.game_state_stack = []

        self.move_counter = 0

    def makeMove(self, move) -> None:

        new_en_passant = 0
        old_castling = (self.game_state_stack[-1] >> 4) & 15
        new_castling = old_castling
        new_draw_move = self.game_state_stack[-1] >> 13

        new_game_state = 0
        pawn_or_taken = False

        piece = self.array[move[0]]
        target_piece = self.array[move[1]]

        self.array[move[1]] = piece
        self.array[move[0]] = 0
        
        self.piece_lists[self.piece_codes[piece & 7]][self.to_move].movePiece(move)

        # pawn move
        if piece & 7 == 1: 
            pawn_or_taken = True

        
        # rook move takes away castling 
        if piece & 7 == 4:
            if move[0] % 8 == 0:

                if self.to_move:
                    new_castling &= 8 + 4 + 2
                else:
                    new_castling &= 8 + 2 + 1

            if move[0] % 8 == 7:

                if self.to_move:
                    new_castling &= 8 + 4 + 1
                else:
                    new_castling &= 4 + 2 +1

        if piece & 7 == 6:
            if self.to_move:
                new_castling &= 8 + 4 
            else:
                new_castling &= 2 + 1
    

        
        # CASTLING
        # queenside
        if move[2] == 6:
            rook = self.array[move[0] - 4]
            self.array[move[0] - 4] = 0
            self.array[move[0] - 1] = rook
            self.piece_lists['rooks'][self.to_move].movePiece([move[0] - 4, move[0] - 1])

        # kingside
        elif move[2] == 5:
            rook = self.array[move[0] + 3]
            self.array[move[0] + 3] = 0
            self.array[move[0] + 1] = rook
            self.piece_lists['rooks'][self.to_move].movePiece([move[0] + 3, move[0] + 1])
        

        
        # EN PASSANT
        # west
        elif move[2] == 4:
            target_piece = self.array[move[0] - 1]
            self.array[move[0] - 1] = 0
            
        # east
        elif move[2] == 3:
            target_piece = self.array[move[0] + 1]
            self.array[move[0] + 1] = 0



        # PAWN PROMOTION
        elif move[2] == 2:
            self.piece_lists[self.piece_codes[piece & 7]][self.to_move].removePiece(move[1])
            self.piece_lists[self.piece_codes[move[3] & 7]][self.to_move].addPiece(move[1])
            self.array[move[1]] = (self.to_move << 3) | move[3]



        # TWO FOWARD
        elif move[2] == 1:            
            new_en_passant = 8 + move[1] % 8



        if target_piece: #piece taken

            if 3 <= move[2] <= 4:
                self.piece_lists[self.piece_codes[1]][self.opponent].removePiece(move[0] + (1 if move[2] == 3 else -1))
            else:
                self.piece_lists[self.piece_codes[target_piece & 7]][self.opponent].removePiece(move[1])
            pawn_or_taken = True

        # change turn
        tmp = self.to_move
        self.to_move = self.opponent
        self.opponent = tmp

        # update gamestate
        self.move_counter += 1
        if pawn_or_taken:
            new_draw_move = 0
        else:
            new_draw_move += 1

        new_game_state |= target_piece
        new_game_state |= (new_castling << 4)
        new_game_state |= (new_en_passant << 9)
        new_game_state |= (new_draw_move << 13)

        self.game_state_stack.append(new_game_state)
        self.stack_index += 1

    def unMakeMove(self, move) -> None:
        last_state = self.game_state_stack.pop()
        captured = last_state & 15
        old_castling = last_state & 240
        old_passant = last_state & 3840
        old_draw = last_state >> 13

        # CASTLING
        # queenside
        if move[2] == 6:
            # move rook
            self.array[move[0] - 4] = self.array[move[0] - 1]
            self.array[move[0] - 1] = 0
            self.array[move[0]] = self.array[move[1]]
            self.array[move[1]] = 0
            self.piece_lists['rooks'][not self.to_move].movePiece([move[0] - 1, move[0] - 4])
            self.piece_lists['kings'][not self.to_move].movePiece([move[1], move[0]])
        # kingside
        elif move[2] == 5:
            # move rook
            self.array[move[0] + 3] = self.array[move[0] + 1]
            self.array[move[0] + 1] = 0
            self.array[move[0]] = self.array[move[1]]
            self.array[move[1]] = 0
            self.piece_lists['rooks'][not self.to_move].movePiece([move[0] + 1, move[0] + 3])
            self.piece_lists['kings'][not self.to_move].movePiece([move[1], move[0]])


        # EN PASSANT
        # west
        elif move[2] == 4:
            piece = self.array[move[1]]
            self.array[move[0]] = piece
            self.array[move[1]] = 0
            self.array[move[0] - 1] = captured
            self.piece_lists[self.piece_codes[piece & 7]][not self.to_move].movePiece([move[1], move[0]])
            self.piece_lists[self.piece_codes[piece & 7]][self.to_move].addPiece(move[0] - 1)
        # east
        elif move[2] == 3:
            piece = self.array[move[1]]
            self.array[move[0]] = piece
            self.array[move[1]] = 0
            self.array[move[0] + 1] = captured
            self.piece_lists[self.piece_codes[piece & 7]][not self.to_move].movePiece([move[1], move[0]])
            self.piece_lists[self.piece_codes[piece & 7]][self.to_move].addPiece(move[0] + 1)


        # PAWN PROMOTION
        elif move[2] == 2:
            piece = self.array[move[1]]
            self.piece_lists[self.piece_codes[piece & 7]][not self.to_move].removePiece(move[1])
            self.array[move[1]] = captured
            self.array[move[0]] = (not self.to_move << 3) | 1
            self.piece_lists['pawns'][not self.to_move].addPiece(move[0])
            if captured:
                self.piece_lists[self.piece_codes[captured & 7]][self.to_move].addPiece(move[1])


        else:
            piece = self.array[move[1]]
            self.array[move[0]] = piece
            self.array[move[1]] = captured
            self.piece_lists[self.piece_codes[piece & 7]][not self.to_move].movePiece([move[1], move[0]])
            if captured:
                self.piece_lists[self.piece_codes[captured & 7]][self.to_move].addPiece(move[1])


        self.stack_index -= 1
        self.move_counter -= 1
        self.opponent = not self.opponent
        self.to_move = not self.to_move

    def loadFEN(self, fen) -> None:

        fields = fen.split(' ')
        pieces = fields[0].split('/')
        to_move = fields[1]
        castling = fields[2]
        en_passant = fields[3]
        draw_move_counter = fields[4]
        fullmove_counter = fields[5]

        game_state = 0

        # array and piece_lists
        for i, row in enumerate(pieces):

            string_pos = 0
            col = 0

            while string_pos < len(row) and col < 8:
                if row[string_pos] in ['0', '1', '2', '3', '4', '5', '6', '7', '8']:
                    col += int(row[string_pos])
                else:
                    if row[string_pos] == 'p':
                        self.array[i * 8 + col] = 9
                        self.piece_lists['pawns'][1].addPiece(i * 8 + col)

                    if row[string_pos] == 'n':
                        self.array[i * 8 + col] = 10
                        self.piece_lists['knights'][1].addPiece(i * 8 + col)

                    if row[string_pos] == 'b':
                        self.array[i * 8 + col] = 11
                        self.piece_lists['bishops'][1].addPiece(i * 8 + col)

                    if row[string_pos] == 'r':
                        self.array[i * 8 + col] = 12
                        self.piece_lists['rooks'][1].addPiece(i * 8 + col)

                    if row[string_pos] == 'q':
                        self.array[i * 8 + col] = 13
                        self.piece_lists['queens'][1].addPiece(i * 8 + col)

                    if row[string_pos] == 'k':
                        self.array[i * 8 + col] = 14
                        self.piece_lists['kings'][1].addPiece(i * 8 + col)

                    if row[string_pos] == 'P':
                        self.array[i * 8 + col] = 1
                        self.piece_lists['pawns'][0].addPiece(i * 8 + col)

                    if row[string_pos] == 'N':
                        self.array[i * 8 + col] = 2
                        self.piece_lists['knights'][0].addPiece(i * 8 + col)

                    if row[string_pos] == 'B':
                        self.array[i * 8 + col] = 3
                        self.piece_lists['bishops'][0].addPiece(i * 8 + col)

                    if row[string_pos] == 'R':
                        self.array[i * 8 + col] = 4
                        self.piece_lists['rooks'][0].addPiece(i * 8 + col)

                    if row[string_pos] == 'Q':
                        self.array[i * 8 + col] = 5
                        self.piece_lists['queens'][0].addPiece(i * 8 + col)

                    if row[string_pos] == 'K':
                        self.array[i * 8 + col] = 6
                        self.piece_lists['kings'][0].addPiece(i * 8 + col)

                    col += 1
                string_pos += 1
                
        # to_move and opponent
        self.to_move = int(to_move == 'b')
        self.opponent = int(not self.to_move)

        # curr game state
        if castling.count('Q'):
            game_state |= (1 << 6)
        if castling.count('K'):
            game_state |= (1 << 7)
        if castling.count('q'):
            game_state |= (1 << 4)
        if castling.count('k'):
            game_state |= (1 << 5)

        if en_passant != '-':
            col = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'].index(en_passant[0])
            game_state |= (col << 8)

        game_state |= (int(draw_move_counter) << 12)
        self.game_state_stack.append(game_state)

        # full move counter
        self.move_counter = int(fullmove_counter) // 2

    def getPieceFEN(self) -> str:
        """ Returns the first 2 fields in the FEN board representation, intented for the UI 
            Will extend later to the while format, to copy and user elsewhere"""

        pieces = ''
        
        for row in range(8):
            empty = 0
            for col in range(8)  :

                piece = self.array[row * 8 + col]
                if piece and empty:
                    pieces += str(empty)
                    empty = 0
                elif not piece:
                    empty += 1

                if piece == 1:
                    pieces += 'P'
                elif piece == 2:
                    pieces += 'N'
                elif piece == 3:
                    pieces += 'B'
                elif piece == 4:
                    pieces += 'R'
                elif piece == 5:
                    pieces += 'Q'
                elif piece == 6:
                    pieces += 'K'

                elif piece == 9:
                    pieces += 'p'
                elif piece == 10:
                    pieces += 'n'
                elif piece == 11:
                    pieces += 'b'
                elif piece == 12:
                    pieces += 'r'
                elif piece == 13:
                    pieces += 'q'
                elif piece == 14:
                    pieces += 'k'

            if empty:
                pieces += str(empty)
            if row // 8 != 7:
                pieces += '/'

        if self.to_move:
            pieces += ' b'
        else:
            pieces += ' w'

        return pieces

    def getAllMoves(self):
        all_moves = self.move_gen.generateAllMoves(self)
        result = 0

        if not len(all_moves):
            if self.move_gen.check:
                result = -1 # loose
            else:
                result = 1 # draw
        
        if self.game_state_stack[-1] >> 13 >= 50:
            result = 1
        
        return all_moves, result