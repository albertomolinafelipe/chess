import numpy as np

class AI:

    def __init__(self) :
        pass

    def makeMove(self, moves):
        return moves[np.random.randint(0, len(moves))]
        
