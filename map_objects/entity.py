import math

import libtcodpy as libtcod
from components.item import Item
from render_functions import RenderOrder


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    def __init__(self, x, y, char, color, name, blocks=False,
                 render_order=RenderOrder.CORPSE,
                 fighter=None, ai=None,
                 item=None, inventory=None,
                 equipment=None, equippable=None,
                 spawner=None,
                 count_value=0, treasure_value=0,
                 stairs=None, level=None, ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.count_value = count_value
        self.treasure_value = treasure_value
        self.item = item
        self.inventory = inventory
        self.stairs = stairs
        self.level = level
        self.equipment = equipment
        self.equippable = equippable
        self.spawner = spawner

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

        if self.stairs:
            self.stairs.owner = self

        if self.level:
            self.level.owner = self

        if self.equipment:
            self.equipment.owner = self

        if self.equippable:
            self.equippable.owner = self
            if not self.item:
                item = Item()
                self.item = item
                self.item.owner = self

        if self.spawner:
            self.spawner.owner = self

    def move(self, dx, dy):
        """
        Move the entity by a given amount
        :param dx: change in x-position
        :param dy: change in y-position
        """
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        """
        Move this entity towards a target in a straight line unless blocked
        :param int target_x: Coordinate to move towards
        :param int target_y: Coordinate to move towards
        :param game_map.GameMap game_map: The map being moved through
        :param list entities: List of things and creatures on the map
        """
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            dx = int(round(dx / distance))
            dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
                get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)

    def move_astar(self, target, entities, game_map):
        """
        Move this entity towards a target.
        :param Entity target: The thing or creature to move towards
        :param list entities: List of things and creatures on the map
        :param game_map.GameMap game_map: The map being moved through
        """
        # Create a FOV map that has the dimensions of the map
        fov = libtcod.map_new(game_map.width, game_map.height)

        # Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                           not game_map.tiles[x1][y1].block_move)

        # Scan all the objects to see if there are objects that must be navigated around
        # Check also that the object isn't self or the target (so that the start and the end points are free)
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                libtcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        my_path = libtcod.path_new_using_map(fov, 1.40)

        # Compute the path between self's coordinates and the target's coordinates
        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths
        # (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around
        # the map if there's an alternative path really far away
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                self.x = x
                self.y = y
        else:
            # Keep the old move function as a backup so that if there are no paths
            # (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            self.move_towards(target.x, target.y, game_map, entities)

            # Delete the path to free memory
        libtcod.path_delete(my_path)

    def distance_to(self, other):
        """
        Calculate the straight-line distance between this Entity and another Entity
        :param Entity other:
        :return int: The distance in tiles
        """
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def distance(self, x, y):
        """
        Calculate the straight-line distance between this entity and a tile on the map
        :param int x: Coordinate of target
        :param int y: Coordinate of target
        :return int: The distance in tiles
        """
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    """
    Return the first Entity which blocks movement at a given x,y coordinate.
    :param list entities: List of things and creatures on the map
    :param int destination_x:
    :param int destination_y:
    :return Entity:
    """
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
