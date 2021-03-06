from enum import Enum

import libtcodpy as libtcod
from game_states import GameStates
from menus import character_screen, inventory_menu, level_up_menu

DISABLE_FOG_OF_WAR = False


class RenderOrder(Enum):
    STAIRS = 1
    CORPSE = 2
    ITEM = 3
    ACTOR = 4


def get_names_under_mouse(mouse, entities, fov_map):
    x = mouse.cx
    y = mouse.cy

    names = [entity.name.capitalize() for entity in entities
             if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names


def get_names_at_position(player, entities):
    names = [entity.name.capitalize() for entity in entities
             if entity.x == player.x and entity.y == player.y
             and entity is not player]
    names = ', '.join(names)

    return names


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '{0}: {1}/{2}'.format(name, value, maximum))


# noinspection PyShadowingNames
def render_all(con, panel, entities, player,
               game_map, fov_map, fov_recompute,
               message_log, screen_width, screen_height,
               bar_width, panel_height, panel_y,
               mouse, colors, game_state):
    """
    Draws all entities in the list
    :param con: The console to draw on
    :param panel: information panel
    :param entities: List of Entity objects
    :param Entity player: The player entity
    :param game_map:  The map of Tiles to draw
    :param fov_map: The map holding Field of View information
    :param fov_recompute:  Need to update the Field of ramView?
    :param MessageLog message_log:
    :param screen_width: width (in chars) of console
    :param screen_height:  height (in chars) of console
    :param bar_width:
    :param panel_height:
    :param panel_y:
    :param libtcod.mouse mouse:
    :param colors: Dictionary of Colors for use with game_map
    :param game_state: Current GameState
    """
    # Draw all the tiles in the game map
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible or DISABLE_FOG_OF_WAR:
                    if wall:
                        libtcod.console_set_char_background(con, x, y,
                                                            colors.get('light_wall'),
                                                            libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y,
                                                            colors.get('light_ground'),
                                                            libtcod.BKGND_SET)
                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(con, x, y,
                                                            colors.get('dark_wall'),
                                                            libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y,
                                                            colors.get('dark_ground'),
                                                            libtcod.BKGND_SET)

    # Draw entities in the list
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    # Clear Player Status and Message Log
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    # Print game messages, one line at a time
    y = 1
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y += 1

    # Draw Player Status
    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               libtcod.light_red, libtcod.darker_red)
    libtcod.console_print_ex(panel, 1, 3, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Dungeon level: {0}'.format(game_map.dungeon_level))
    libtcod.console_print_ex(panel, 1, 5, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Treasure: {0}'.format(player.treasure_value))

    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                             get_names_under_mouse(mouse, entities, fov_map))
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                             get_names_at_position(player, entities))

    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)

    # Draw Inventory Menu
    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
        else:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'

        inventory_menu(con, inventory_title, player, 50, screen_width, screen_height)
    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(con, 'Level Up!  Choose a stat to raise:', player, 40, screen_width, screen_height)
    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 10, screen_width, screen_height)


def clear_all(con, entities):
    """
    Erases, from screen, all entities in the list
    :param con: The console to draw on
    :param entities: List of Entity objects
    """
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map, game_map):
    """
    Draw the character that represents this object
    :param con: The console to draw on
    :param entity: Entity object to clear
    :param fov_map: The map holding Field of View information
    :param game_map: The map holding game tiles
    """
    if DISABLE_FOG_OF_WAR or libtcod.map_is_in_fov(fov_map, entity.x, entity.y) or (
            entity.stairs and game_map.tiles[entity.x][entity.y].explored):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    """
    Erase, from the screen, an object representation
    :param con: The console to draw on
    :param entity: Entity object to clear
    """
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
