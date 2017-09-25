from random import randint

import libtcodpy as libtcod
from components.stairs import Stairs
from game_messages import Message
from map_objects.entity import Entity
from map_objects.item_factory import ItemFactory
from map_objects.monster_factory import MonsterFactory
from map_objects.map_room import Room
from map_objects.spawner_factory import SpawnerFactory
from map_objects.tile import Tile
from random_utils import from_dungeon_level
from render_functions import RenderOrder


class GameMap:
    """
    Game Map
    Tracks location and state of all tiles
    Performs random map generation
    """

    def __init__(self, width, height, monster_dict, item_dict, dungeon_level=1):
        """
        Create a new Game Map
        :param width: Width of map in tiles
        :param height: Height of map in tiles
        :param monster_dict:
        :param dungeon_level:
        """
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.monster_dict = monster_dict
        self.item_dict = item_dict
        self.dungeon_level = dungeon_level

        self.monster_chances = {}
        for key, settings in monster_dict.items():
            self.monster_chances[key] = from_dungeon_level(settings['likelihood'], dungeon_level)

        self.item_chances = {}
        for key, settings in item_dict.items():
            self.item_chances[key] = from_dungeon_level(settings['likelihood'], dungeon_level)

    # noinspection PyUnusedLocal
    def initialize_tiles(self, default_block=True):
        tiles = [[Tile(default_block) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities):
        """
        Create a random map
        :param int max_rooms:
        :param int room_min_size:
        :param int room_max_size:
        :param int map_width:
        :param int map_height:
        :param Entity player:
        :param list entities:
        """

        rooms = []
        num_rooms = 0
        center_of_last_room_x = None
        center_of_last_room_y = None

        for r in range(max_rooms):
            # Generate a room
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)
            new_room = Room(x, y, w, h)

            for other_room in rooms:
                # If the room overlaps an existing room try again
                if new_room.intersect(other_room):
                    break
            # If the room placement is legal
            else:
                self.create_room(new_room)
                (new_x, new_y) = new_room.center()
                center_of_last_room_x = new_x
                center_of_last_room_y = new_y
                is_first_room = False

                # If this is the first room, start the player there.
                if num_rooms == 0:
                    is_first_room = True
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

                self.place_entities(new_room, entities, is_first_room)
                # Add room to list
                rooms.append(new_room)
                num_rooms += 1

        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', libtcod.white, 'Stairs',
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)

    def create_room(self, room):
        """
        Add a room to the map and set tiles in a room to be Passable
        :param Room room: a room-defining rectangle
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

    def place_entities(self, room, entities, is_first_room):
        """
        Set some random monsters in this room
        :param room: The room rectangle to add monsters
        :param entities: A list of monsters and their locations in the map
        :param is_first_room: Is this the first room in the maze.
        """
        # TODO: Load from Game Settings
        max_monsters_per_room = from_dungeon_level([[4, 1], [7, 4], [10, 6]], self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], self.dungeon_level)

        room.monster_limit = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        if not is_first_room:
            monster_count = 0
            while monster_count < room.monster_limit:
                x, y = room.random_point()
                monster = MonsterFactory.get_monster(self.monster_dict, self.monster_chances,
                                                     entities, x, y)
                if monster and monster_count + monster.count_value <= room.monster_limit:
                    entities.append(monster)
                    monster_count += monster.count_value

            # TODO: Clean This Up
            if randint(0, 2) == 0:
                x, y = room.random_point()
                spawner = SpawnerFactory.get_monster_spawner(self.monster_dict, self.monster_chances,
                                                             entities, x, y, room)
                entities.append(spawner)

        item_count = 0
        while item_count < number_of_items:
            x, y = room.random_point()
            item = ItemFactory.get_item(self.item_dict, self.item_chances, entities, x, y)
            if item and item_count + item.count_value <= number_of_items:
                entities.append(item)
                item_count += item.count_value

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

    def next_floor(self, player, message_log, constants):
        """
        Prepare the next level of the dungeon
        :param Entity player: the Player (@)
        :param game_messages.MessageLog message_log:game message log
        :param dict constants: Game constants
        :return list: entities on map
        """
        self.dungeon_level += 1
        entities = [player]
        self.tiles = self.initialize_tiles(True)
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)

        player.fighter.heal(player.fighter.max_hp // 2)
        message_log.add_message(Message('You take a moment to rest and recover your strength.', libtcod.violet))

        return entities
