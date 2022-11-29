from ai import AI
from controller import Controller
import time

ai = AI(Controller(), 1)
board0 = ['R',  'N',  'B',  'Q',  'K',  'B',  'N',  'R',
          'P0', 'P0', 'P0', 'P0', 'P0', 'P0', 'P0', 'P0', 
          '0',  '0',  '0',  '0',  '0',  '0',  '0',  '0', 
          '0',  '0',  '0',  '0',  '0',  '0',  '0',  '0',
          '0',  '0',  '0',  '0',  '0',  '0',  '0',  '0',
          '0',  '0',  '0',  '0',  '0',  '0',  '0',  '0',
          'p0', 'p0', 'p0', 'p0', 'p0', 'p0', 'p0', 'p0', 
          'r',  'n',  'b',  'q',  'k',  'b',  'n',  'r',
          '3','3','0','0','3']

board0 = ai.ctrl.codeBoard(board0)

for i in [3]:
    start = time.time()
    print(ai.chooseMove(board0, depth=i))
    print(ai.moves_searched)
    print(time.time() - start)
