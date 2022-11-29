import numpy as np

class AI:
    def __init__(self, controller, lvl):
        self.ctrl = controller
        self.lvl = lvl
        self.moves_searched = 0

    def chooseMove(self, board, depth=0):

        self.moves_searched = 0

        # Random
        if self.lvl == 0:
            moves = self.ctrl.getMoves(board)
            return moves[np.random.randint(0, len(moves))], None

        if self.lvl == 1:
            return self.searchAndEvaluate(board, depth)
    
    def searchAndEvaluate(self, board, depth):
        """ Search and pick the board with highest calculated value """

        # Value of each piece, my own input
        piece_values = [1,3,3,5,9,0]
        value_board = self.evaluate(board)
        return self.search(board, depth, func=self.evaluate, first=True)
    
    def evaluate(self, board):
        """ Returns value of the board with the piece values """
        # Value of each piece, my own input
        color = board[-2]
        piece_values = {
            '1' : 1,
            '2' : 3,
            '3' : 3,
            '4' : 5,
            '5' : 9,
            '6' : 0,
        }
        value_board = 0
        for tile in board[:-5]:
            if tile != '3':
                if tile[-1] != color:
                    value_board -= piece_values[tile[-2]]
                else:
                    value_board += piece_values[tile[-2]]
        return value_board

    def search(self, board, depth, func=None, first=False):
        """ Returns the move that gets to the best board in #depth moves
        assuming the other player chooses their board optimally with the same func """
        
        moves = self.ctrl.getMoves(board)
        best_evaluation = - np.inf

        # If its the first search we want to return the move with the best val
        if first: 
            best_move = None
            for move in moves:
                move_made = self.ctrl.makeMove(move, np.copy(board))
                evaluation = - self.search(move_made, depth-1, func=func)
                if evaluation > best_evaluation:
                    best_evaluation = evaluation
                    best_move = move
            return best_move
        
        # If its not the first search we just want the best value
        else:
            if depth == 0:
                self.moves_searched += 1
                return func(board)

            if len(moves) == 0:
                if self.ctrl.lookForCheck(board):
                    return - np.inf
                else:
                    return 0 # Value of draw

            for move in moves:
                move_made = self.ctrl.makeMove(move, np.copy(board))
                evaluation =  - self.search(move_made, depth-1, func=func)
                best_evaluation = max(best_evaluation, evaluation)


        return best_evaluation