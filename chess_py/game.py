from board import Board
from ui import UI
from ai import AI


start_board_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
test = '4k3/8/8/8/8/8/P7/1N2K1N1 w KQkq - 0 1'

class Game:

    def __init__(self):
        self.board = Board()
        self.ui = UI()
        self.ai = AI()
        self.ai_settings, self.ai_player = self.ui.getPreGame(self.board.array)
        if self.ai_player != -1:
            self.board.loadFEN(start_board_fen)
            self.play()

    def play(self):
        move = []
        while True:

            turn = self.board.to_move
            all_moves, result = self.board.getAllMoves()


            if result:
                break
            
            # AI PLAYER
            if turn in self.ai_player:
                new_move, diagnostics = self.ai.getMove(self.board, all_moves, self.ai_settings[turn])

                # If window is closed while looking for move
                if new_move == -1:
                    break

                self.ui.handleStacks(self.board.array.copy(), move, len(all_moves), self.board)

                self.board.makeMove(new_move)
                move = new_move
                
                out = self.ui.display(self.board.array.copy(), 
                                    turn=self.board.to_move, 
                                    move=move,
                                    board_debug=self.board,
                                    ai_diag=diagnostics)
                if out == -1:
                    break

            # USER
            else:
                move = self.ui.display(self.board.array.copy(), 
                                        turn=self.board.to_move, 
                                        move=move, 
                                        selection=True,
                                        all_moves=all_moves,
                                        board_debug=self.board)
                # If window is closed while looking for move
                if move == -1:
                    return move, None

                self.board.makeMove(move)


        
        if result:
            self.ui.display(self.board.array.copy(), 
                                        turn=self.board.to_move, 
                                        move=move, 
                                        selection=True,
                                        all_moves=all_moves,
                                        board_debug=self.board,
                                        result=result)


if __name__ == '__main__':
    Game()