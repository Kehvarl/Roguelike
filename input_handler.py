import libtcodpy as libtcod


def handle_keys(key):
    """

    :param libtcon.Key key: Keypress performed by player
    :return dictionary: Command to perform
    """
    # Movement Keys
    if key.vk == libtcod.KEY_UP:
        return _move(0, -1)
    elif key.vk == libtcod.KEY_DOWN:
        return _move(0, 1)
    elif key.vk == libtcod.KEY_LEFT:
        return _move(-1, 0)
    elif key.vk == libtcod.KEY_RIGHT:
        return _move(1, 0)

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
