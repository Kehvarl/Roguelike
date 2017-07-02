from map_objects.tile import  Tile


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]

        tiles[30][22].block()
        tiles[31][22].block()
        tiles[32][22].block()

        return tiles

    def is_blocked(self, x, y):
        if self.tiles[x][y].block_move:
            return True

        return False
