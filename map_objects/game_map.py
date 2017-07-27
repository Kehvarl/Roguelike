from random import randint

import libtcodpy as libtcod
from components.ai import BasicMonster
from components.fighter import Fighter
from components.item import Item
from entity import Entity
from map_objects.rectangle import Rect
from map_objects.tile import Tile
from render_functions import RenderOrder


class GameMap:
    """
    Game Map
    Tracks location and state of all tiles
    Performs random map generation
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self, default_block=True):
        tiles = [[Tile(default_block) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities,
                 max_monsters_per_room=0, max_items_per_room=0):
        """
        Create a random map
        :param int max_rooms:
        :param int room_min_size:
        :param int room_max_size:
        :param int map_width:
        :param int map_height:
        :param Entity player:
        :param list entities:
        :param int max_monsters_per_room:
        :param int max_items_per_room:
        """

        rooms = []
        num_rooms = 0
        for r in range(max_rooms):
            # Generate a room
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)
            new_room = Rect(x, y, w, h)

            for other_room in rooms:
                # If the room overlaps an existing room try again
                if new_room.intersect(other_room):
                    break
            # If the room placement is legal
            else:
                self.create_room(new_room)
                (new_x, new_y) = new_room.center()

                # If this is the first room, start the player there.
                if num_rooms == 0:
                    player.x = new_x
                    player.y = new_y
                else:
                    # If it's not the first room  connect it to an existing room.

                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    # Randomly determine corridor arrangement.
                    if randint(0, 1) == 1:
                        # Horizontal tunnel, then Vertical
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # Vertical tunnel, then Horizontal
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, entities, max_monsters_per_room, max_items_per_room)
                # Add room to list
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room):
        """
        Add a room to the map and set tiles in a room to be Passable
        :param Rect room: a room-defining rectangle
        """
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].block(False)

    def create_h_tunnel(self, x1, x2, y):
        """
        Create a tunnel
        :param int x1: Start of Tunnel
        :param int x2: End of Tunnel
        :param int y: The y position of the tunnel
        """
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].block(False)

    def create_v_tunnel(self, y1, y2, x):
        """
        Create a vertical tunnel
        :param int y1: Start of Tunnel
        :param int y2: End of Tunnel
        :param int x: X position of the tunnel
        """
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].block(False)

    def place_entities(self, room, entities, max_monsters_per_room=0, max_items_per_room=0):
        """
        Set some random monsters in this room
        :param room: The room rectangle to add monsters
        :param entities: A list of monsters and their locations in the map
        :param max_monsters_per_room: Limit to monsters in a room
        :param max_items_per_room: Limit to items in a room
        """
        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        for i in range(number_of_monsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    fighter_component = Fighter(hp=10, defense=0, power=3)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'o', libtcod.desaturated_green, 'Orc', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

                else:
                    fighter_component = Fighter(hp=16, defense=1, power=4)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'T', libtcod.darker_green, 'Troll', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

                entities.append(monster)

        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_component = Item()
                item = Entity(x, y, '!', libtcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM,
                              item=item_component)

                entities.append(item)

    def is_blocked(self, x, y):
        """
        Check to see if a tile blocks movement
        :param int x:
        :param int y:
        :return boolean: True if tile blocks movement
        """
        if self.tiles[x][y].block_move:
            return True

        return False
