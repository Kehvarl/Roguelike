import libtcodpy as libtcod
import json
from components.equipable import Equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Entity, RenderOrder
from equipment_slots import EquipmentSlots
from game_messages import MessageLog
from game_states import GameStates
from map_objects.game_map import GameMap


def get_constants():
    """
    Manage all the core game settings
    :return dict: initial game constants
    """
    window_title = "Roguelike Tutorial Revised"
    # Screen Size
    screen_width = 80
    screen_height = 50
    # HP status bar
    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height
    # Message box
    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1
    # Map size
    map_width = 80
    map_height = 43
    # Room size and count
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    # Field-of=View settings
    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    # Usable Colors
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    # Load Monsters from file
    with open('settings/monsters.json') as json_data:
        monster_dict = json.load(json_data)

    # Convert settings to passable dictionary
    constants = {
        'window_title': window_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'map_width': map_width,
        'map_height': map_height,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'colors': colors,
        'monster_dict': monster_dict
    }

    return constants


def get_game_variables(constants):
    # Initial Player and NPC locations
    # center_x = int(screen_width / 2)
    # center_y = int(screen_height / 2)
    fighter_component = Fighter(hp=100, defense=1, power=2)
    inventory_component = Inventory(26)
    level_component = Level()
    equipment_component = Equipment()
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component, level=level_component,
                    equipment=equipment_component)
    entities = [player]

    # Starting Equipment
    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=2)
    dagger = Entity(0, 0, '-', libtcod.sky, 'Dagger', equippable=equippable_component)
    player.inventory.add_item(dagger)
    player.equipment.toggle_equip(dagger)

    # Generate Game Map
    game_map = GameMap(constants['map_width'], constants['map_height'], constants['monster_dict'])
    game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)

    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state
