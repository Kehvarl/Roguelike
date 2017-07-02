import libtcodpy as libtcod

def render_all(con, entities, screen_width, screen_height):
    """
    Draws all entities in the list
    :param con: The console to draw on
    :param entities: List of Entity objects
    :param screen_width: width (in chars) of console
    :param screen_height:  height (in chars) of console
    """
    for entity in entities:
        draw_entity(con, entity)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
    """
    Erases all entities in the list
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
    Erase the character that represents this object
    :param con: The console to draw on
    :param entity: Entity object to clear
    """
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)