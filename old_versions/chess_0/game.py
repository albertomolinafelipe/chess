import pygame as pg
import numpy as np
from piece import Pawn, Bishop, Rook, Knight, King, Queen

colors = {
    'brown' : (165, 122, 113),
    'beige' : (245, 236, 234),
    'lblue' : (149, 178, 222),
    'dblue' : (102, 149, 222),
    'lred' : (227, 108, 99),
    'dred': (227, 82, 71),
    'black' : (0, 0, 0)
}

class Game:
    def __init__(self, size=480):
        self.size = size
        self.running = True
        self.board = self.boardInit()
        self.piece_selected = None
        self.turn = 'w'
        self.kings = []

        pg.init()
        self.screen = pg.display.set_mode((size, size)) 
        pg.display.set_caption("CHESS_0: white's turn")
            
    def boardInit(self):
        """ Creates the board at the beginning of the game"""
        arr = np.full([8,8], None)
        # A1 bottom left
        for i in range(8):
            # pawns
            arr[1][i] = Pawn('b', 1, i, arr)
            arr[6][i] = Pawn('w', 6, i, arr)

        # rooks
        arr[0][0] = Rook('b', 0, 0, arr)
        arr[0][7] = Rook('b', 0, 7, arr)
        arr[7][0] = Rook('w', 7, 0, arr)
        arr[7][7] = Rook('w', 7, 7, arr)
        # knights
        arr[0][1] = Knight('b', 0, 1, arr)
        arr[0][6] = Knight('b', 0, 6, arr)
        arr[7][1] = Knight('w', 7, 1, arr)
        arr[7][6] = Knight('w', 7, 6, arr)
        # bishop
        arr[0][2] = Bishop('b', 0, 2, arr)
        arr[0][5] = Bishop('b', 0, 5, arr)
        arr[7][2] = Bishop('w', 7, 2, arr)
        arr[7][5] = Bishop('w', 7, 5, arr)
        # queen
        arr[0][3] = Queen('b', 0, 3, arr)
        arr[7][3] = Queen('w', 7, 3, arr)
        #kings
        arr[0][4] = King('b', 0, 4, arr)
        arr[7][4] = King('w', 7, 4, arr)

        # Scale the images
        for row in arr:
            for piece in row:
                if piece is not None:
                    piece.img = pg.transform.scale(piece.img,\
                        (int(self.size/8), int(self.size/8)))
        return arr

    def switchTurn(self):
        if self.turn == 'w':
            self.turn = 'b'
        elif self.turn == 'b':
            self.turn = 'w'
        self.piece_selected.moved = True
        self.piece_selected.selected = False
        self.piece_selected = None

    def moveMade(self, py, px):
        # if pawn reaches end
        if self.piece_selected.pawn and ( \
            (self.piece_selected.color == 'b' and py == 7) or\
            (self.piece_selected.color == 'w' and py == 0)):
            self.piece_selected.move(py, px)
            self.board[py, px] = Queen(self.piece_selected.color, py, px, self.board)
            self.board[py, px].moved = True
        else:
            self.piece_selected.move(py, px)
        self.switchTurn()

    def click(self, px, py):
        """ Changes the piece selected and moves"""
        # Choose a piece
        if self.piece_selected is None:
            if self.board[py][px] is not None and self.board[py][px].color == self.turn:
                self.piece_selected = self.board[py][px]
                self.piece_selected.updateMoves()
                self.piece_selected.selected = True
        else:
            # Make a move
            if [py,px] in self.piece_selected.moves:
                self.moveMade(py, px)

            # change selection
            elif self.board[py][px] is not None and self.board[py][px].color == self.turn:
                # cambiar la seleccionada
                self.piece_selected.selected = False
                self.piece_selected = self.board[py][px]
                self.piece_selected.updateMoves()
                self.piece_selected.selected = True                

    def draw(self):
        """ Displays the board"""
        # board and moves
        tmp = 0
        for j in range(8):
            for i in range(8):
                rect = (i * self.size/8, j * self.size/8, self.size/8, self.size/8)
                if (i+ j*8 + tmp) % 2 == 0:
                    pg.draw.rect(self.screen, colors['beige'], rect)
                else:
                    pg.draw.rect(self.screen, colors['brown'], rect)
                if self.piece_selected is not None:
                    if [j, i] in self.piece_selected.moves:
                        if (i+ j*8 + tmp) % 2 == 0:
                            pg.draw.rect(self.screen, colors['lblue'], rect)
                        else:
                            pg.draw.rect(self.screen, colors['dblue'], rect)
            tmp += 1

        tmp = 0
        for j, row in enumerate(self.board):
            for i, piece in enumerate(row):
                rect = (i * self.size/8, j * self.size/8, self.size/8, self.size/8)

                # pieces
                if piece is not None:
                    if piece.selected:
                        # if selected
                        if (i+ j*8 + tmp) % 2 == 0:
                            pg.draw.rect(self.screen, colors['lred'], rect)
                        else:
                            pg.draw.rect(self.screen, colors['dred'], rect)
                    self.screen.blit(piece.img, (piece.col * self.size/8, piece.row * self.size/8))

                # lines
                pg.draw.rect(self.screen, colors['black'], rect, 1)
            tmp += 1

        pg.display.flip()

    def run(self):
        while self.running:
            self.draw()
            if self.turn == 'w':
                pg.display.set_caption("CHESS: white's turn")
            else:
                pg.display.set_caption("CHESS: black's turn")
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    px = int(event.pos[0] // (self.size/8))
                    py = int(event.pos[1] // (self.size/8))
                    self.click(px, py)
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()

    def lookForCheck(self):
        # Primero solo el check de ataque, es decir, si tu rey ya está en peligro
        pass


def main():
    Game().run()

if __name__ == '__main__':
    main()