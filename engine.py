import libtcodpy as libtcod
from entity import Entity
from render_functions import clear_all, render_all
from map_objects.game_map import GameMap
import input_handler


def main():
    # Define some basic game settings
    # Screen Size
    screen_width = 80
    screen_height = 50
    # Map size
    map_width = 80
    map_height = 45
    # Room size and count
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    # Usable Colors
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150)
    }

    # Initial Player and NPC locations
    center_x = int(screen_width / 2)
    center_y = int(screen_height / 2)
    player = Entity(center_x, center_y, '@', libtcod.white)
    npc = Entity(center_x-5, center_y, '@', libtcod.yellow)
    entities = [npc, player]

    # Setup Display
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)
    # Create Main Window/Console
    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised (Py3)', False)
    con = libtcod.console_new(screen_width, screen_height)

    # Generate Game Map
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player)

    # Setup Input Devices
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Game Loop
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        # Render Entities on Map
        render_all(con, entities, game_map, screen_width, screen_height, colors)
        libtcod.console_flush()

        clear_all(con, entities)
        # Get Player Input
        action = input_handler.handle_keys(key)
        move = action.get('move')
        game_exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        # Perform needed actions
        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)

        if game_exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()
