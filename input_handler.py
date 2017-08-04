import libtcodpy as libtcod
from game_states import GameStates


def handle_keys(key, game_state):
    """

    :param libtcod.Key key: Keypress performed by player
    :param GameState game_state: which game state we're currently in
    :return dictionary: Command to perform
    """
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)

    return {}


def handle_targeting_keys(key):
    """

    :param libtcod.Key key: Keypress performed by player
    :return dictionary: Command to perform
    """
    # ESC: exit the game
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    # Any other keypress: do nothing
    return {}


def handle_player_turn_keys(key):
    """

    :param libtcod.Key key: Keypress performed by player
    :return dictionary: Command to perform
    """
    key_char = chr(key.c)

    # Movement Keys
    if key.vk == libtcod.KEY_UP or key_char == 'k':
        return _move(0, -1)
    elif key.vk == libtcod.KEY_DOWN or key_char == 'j':
        return _move(0, 1)
    elif key.vk == libtcod.KEY_LEFT or key_char == 'h':
        return _move(-1, 0)
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'l':
        return _move(1, 0)
    elif key_char == 'y':
        return _move(-1, -1)
    elif key_char == 'u':
        return _move(1, -1)
    elif key_char == 'b':
        return _move(-1, 1)
    elif key_char == 'n':
        return _move(1, 1)

    # Pick up items
    if key_char == 'g':
        return {'pickup': True}

    # Inventory Management
    elif key_char == 'i':
        return {'show_inventory': True}
    elif key_char == 'd':
        return {'drop_inventory': True}

    # Alt+Enter: toggle full screen
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}

    # ESC: exit the game
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    # Any other keypress: do nothing
    return {}


def handle_player_dead_keys(key):
    """

    :param libtcod.Key key: Keypress performed by player
    :return dictionary: Command to perform
    """
    key_char = chr(key.c)

    # Show Inventory
    if key_char == 'i':
        return {'show_inventory': True}

    # Alt+Enter: toggle full screen
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}

    # ESC: exit the game
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    # Any other keypress: do nothing
    return {}


def handle_inventory_keys(key):
    """

    :param libtcod.Key key: Keypress performed by player
    :return dictionary: Command to perform
    """
    index = key.c - ord('a')

    if index >= 0:
        return {'inventory_index': index}

    # Alt+Enter: toggle full screen
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}

    # ESC: exit the game
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}


def handle_main_menu(key):
    key_char = chr(key.c)

    if key_char == 'a':
        return {'new_game': True}
    elif key_char == 'b':
        return {'load_game': True}
    elif key_char == 'c' or key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}


def handle_mouse(mouse):
    """

    :param libtcod.Mouse mouse:
    :return: dict: Command to perform
    """
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}


def _move(dx, dy):
    """
    Convert coordinate change to Movement Command for game engine
    :param dx:
    :param dy:
    :return dictionary: Movement Command
    """
    return {'move': (dx, dy)}

