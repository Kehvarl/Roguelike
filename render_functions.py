import libtcodpy as libtcod


def render_all(con, entities, game_map, screen_width, screen_height, colors):
    """
    Draws all entities in the list
    :param con: The console to draw on
    :param entities: List of Entity objects
    :param game_map:  The map of Tiles to draw
    :param screen_width: width (in chars) of console
    :param screen_height:  height (in chars) of console
    :param colors: Dictionary of Colors for use with game_map
    """
    # Draw all the tiles in the game map
    for y in range(game_map.height):
        for x in range(game_map.width):
            if game_map.tiles[x][y].block_sight:
                libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)

    # Draw entities in the list
    for entity in entities:
        draw_entity(con, entity)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
    """
    Erases, from screen, all entities in the list
    :param con: The console to draw on
    :param entities: List of Entity objects
    """
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity):
    """
    Draw the character that represents this object
    :param con: The console to draw on
    :param entity: Entity object to clear
    """
    libtcod.console_set_default_foreground(con, entity.color)
    libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    """
    Erase, from the screen, an object representation
    :param con: The console to draw on
    :param entity: Entity object to clear
    """
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)