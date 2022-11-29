from engine import Engine
from user_interface import UserInterface
import time

starting_board = [
[36028797018963968 ,
18014398509481984,
9007199254740992,
4503599627370496,
2251799813685248,
1125899906842624,
562949953421312,
281474976710656 ],
[4611686018427387904,
144115188075855872],
[2305843009213693952,
288230376151711744],
[9223372036854775808,
72057594037927936 ],
[1152921504606846976 ],
[576460752303423488],
[32768,
16384,
8192,
4096,
2048,
1024,
512,
256],
[64,
2],
[32,
4],
[128,
1],
[16],
[8],
[0,0,0,0,3]]

test = [
[0 ,
0,
0,
0,
0,
0,
0,
0 ],
[0,
0],
[0,
0],
[0,
0 ],
[0 ],
[576460752303423488],
[0,
0,
0,
0,
0,
0,
0,
0],
[0,
0],
[0,
0],
[0,
0],
[0],
[8],
[0,0,0,0,3]]


board = test

engine = Engine()
ui = UserInterface()
ui.getUserInfo()
move = []
ui.display(board, [], [])
for x in range(10):
    move = ui.display(board, engine.getAllMoves(board), move, selection=True)
    print('\n\n')
    info = engine.makeMove(board, move)
    ui.display(board, [], move)
    
