
from tracemalloc import start
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


# depth and alpha beta pruning, move ordering
strategy = [3, True, False]

class Game:
    def __init__(self) -> None:
        self.engine = Engine(strategy)
        self.ui = UserInterface()
        user_info = self.ui.getUserInfo()
        if user_info != -1:
            self.play(test, user_info)
    
    def play(self, board, user_info):
        move = []
        while True:
            turn = board[-1][-2]
            all_moves = self.engine.getAllMoves(board)

            if board[-1][-1] != 3:
                break

            if turn in user_info:
                move = self.ui.display(board, all_moves, move, selection=True)
            else:
                start = time.time()
                move = self.engine.getMove(board, all_moves)
                print('AI took', time.time()-start)
                print('It checked', self.engine.positions_checked, 'at depth', self.engine.depth)
                print()
            if move == -1:
                break

            self.engine.makeMove(board, move)
            self.ui.display(board, [], move)
        if move != -1:
            self.ui.display(board, [], move, selection=True, end=True)


def main():
    Game()

if __name__ == '__main__':
    main()