class Tile:
    """
    A Tile on a map.  It may or may not block movement and may or may not block line of sight
    """
    def __init__(self, block_move=False, block_sight=None):
        self.block_move = block_move

        if block_sight is None:
            self.block_sight = block_move
        else:
            self.block_sight = block_sight

    def block(self, state=True):
        """
        Set the blocking (movement and sight) state of this tile
        :param boolean state: The desired blocking state
        """
        self.block_sight = state
        self.block_move = state
