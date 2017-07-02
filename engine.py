import libtcodpy as libtcod
from entity import Entity
from render_functions import clear_all, render_all
import input_handler


def main():
    screen_width = 80
    screen_height = 50

    center_x = int(screen_width / 2)
    center_y = int(screen_height / 2)
    player = Entity(center_x, center_y, '@', libtcod.white)
    npc = Entity(center_x-5, center_y, '@', libtcod.yellow)

    entities = [npc, player]

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised (Py3)', False)

    con = libtcod.console_new(screen_width, screen_height)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        render_all(con, entities, screen_width, screen_height)
        libtcod.console_flush()

        clear_all(con, entities)

        action = input_handler.handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            player.move(dx, dy)

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()
