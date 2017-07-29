import libtcodpy as libtcod


def handle_keys(key):
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

    # Show Inventory
    elif key_char == 'i':
        return {'show_inventory': True}

    # Alt+Enter: toggle full screen
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}

    # ESC: exit the game
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    # Any other keypress: do nothing
    return {}


def _move(dx, dy):
    """
    Convert coordinate change to Movement Command for game engine
    :param dx:
    :param dy:
    :return dictionary: Movement Command
    """
    return {'move': (dx, dy)}
