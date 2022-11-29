import random
import numpy as np
import time


class AI:

    def __init__(self) -> None:
        self.piece_values = [0, 1, 3, 3, 5, 9, 0]
        self.positions = 0

    def getMove(self, board, all_moves, how):

        start = time.time()

        depth = 2
        alpha = False
        montecarlo = True
        zobrist = True

        

        if how == 1:
            move = all_moves[random.randint(0, len(all_moves)-1)]

        if how == 2:
            move = self.search(board, all_moves, depth)

        diagnostics = [
            round(time.time()-start, 5),
            depth, 
            self.positions,
            alpha,
            montecarlo,
            zobrist
        ]

        return move, diagnostics

    def search(self, board, all_moves, depth) -> list:

        best_eval = -np.inf
        best_move = None

        for move in all_moves:
            board.makeMove(move)
            
            evaluation = -self._search(board, depth-1)
            board.unMakeMove(move)

            if evaluation > best_eval:
                best_eval = evaluation
                best_move = move

        return best_move

    def _search(self, board, depth):

        self.positions += 1
        
        if not depth:
            return self.evaluate(board, board.to_move)

        all_moves, result = board.getAllMoves()
        
        if result == -1:
            return -np.inf

        best_eval = -np.inf

        for move in all_moves:
            board.makeMove(move)
            evaluation = -self._search(board, depth-1)
            board.unMakeMove(move)

            if evaluation > best_eval:
                best_eval = evaluation
        
        return best_eval

    def evaluate(self, board, turn):

        ret = 0
        
        for tile in board.array:

            if tile:
                if tile >> 3:
                    ret -= self.piece_values[tile&7]
                else:
                    ret += self.piece_values[tile&7]

        if turn:
            ret = - ret
        
        return ret


