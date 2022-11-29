import numpy as np
from interface import UI
from controller import Controller
from ai import AI
import time

normal = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R',
          'P0', 'P0', 'P0', 'P0', 'P0', 'P0', 'P0', 'P0', 
          '0', '0', '0', '0', '0', '0', '0', '0', 
          '0', '0', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0', '0', '0', '0',
          'p0', 'p0', 'p0', 'p0', 'p0', 'p0', 'p0', 'p0', 
          'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r',
          '3','3','0','0','3']

start = np.array(normal, dtype=np.object_)

class Game:
    def __init__(self):
        # self.p1 = [False/True player/ai, AI/None if AI]
        self.white = None
        self.black = None
        self.ctrl = Controller()
        self.ui = UI(480, self.ctrl)
        self.preGame()
    def preGame(self):
        self.white, self.black = self.ui.getPreGame()
        if self.white != -1:
            self.white = [self.white, None]
            self.black = [self.black, None]
            if self.white[0]:
                self.white[1] = AI(self.ctrl, 0)
            if self.black[0]:
                self.black[1] = AI(self.ctrl, 0)
            self.turnManager()

    def turnManager(self):
        board = self.ctrl.codeBoard(start)
        while True:
            #all_moves = self.ctrl.getMoves(board)

            move = self.chooseMove(board)
            if move == -1:
                break
            self.ctrl.changeResult(board)
            if not self.keepPlaying(board):
                self.ui.getMove([], board, ai_move=None, end=True)
                break

            self.ctrl.makeMove(move, board)
                   
    def chooseMove(self, board):
        if board[-2] == '0':
            if self.white[0]:
                move = self.white[1].chooseMove(board)
                if self.ui.getMove([], board, ai_move=move):
                    move = -1
                self.ui.last_move = move
            else:
                move = self.ui.getMove(self.ctrl.getMoves(board), board)
        else:
            if self.black[0]:
                move = self.black[1].chooseMove(board)
                if self.ui.getMove([], board, ai_move=move):
                    move = -1
                self.ui.last_move = move
            else:
                move = self.ui.getMove(self.ctrl.getMoves(board), board)
        return move

    def keepPlaying(self, board):
        ret = True
        if board[-1] == '2':
            ret = False
        if board[-1] == '1':
            ret = False
        if board[-1] == '0':
            ret = False
        return ret
        

def main():
    Game()

if __name__ == '__main__':
    main()