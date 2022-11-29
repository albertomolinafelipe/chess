
class PieceList:

    def __init__(self, max_capacity):
        self.occupied_tiles = [None for x in range(max_capacity)]
        self.map = [0 for x in range(64)]
        self.count = 0

    def addPiece(self, tile):
        self.occupied_tiles[self.count] = tile
        self.map[tile] = self.count
        self.count += 1

    def removePiece(self, tile):
        piece_index = self.map[tile]
        self.occupied_tiles[piece_index] = self.occupied_tiles[self.count - 1]
        self.map[self.occupied_tiles[piece_index]] = piece_index
        self.count -= 1

    def movePiece(self, move):
        piece_index = self.map[move[0]]
        self.occupied_tiles[piece_index] = move[1]
        self.map[move[1]] = piece_index


