import libtcodpy as libtcod


def menu(con, header, options, width, screen_width, screen_height):
    """
    Draw a Menu
    :param libtcod.console con: Console to draw menu on
    :param header:
    :param list options: Items to show in Menu
    :param int width: Width of menu in tiles
    :param int screen_width: Screen size
    :param int screen_height: Screen size
    """
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)

    # print the header with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ')' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    # blit the contents of the "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)


def inventory_menu(con, header, player, inventory_width, screen_width, screen_height):
    """
    Draw a menu displaying inventory contents
    :param libtcod.console con: Console to draw menu on
    :param header:
    :param Entity player: Entity with Inventory to display
    :param int inventory_width: Width of the Inventory Menu in tiles
    :param int screen_width: Screen size
    :param int screen_height: Screen size
    """
    # show a menu with each item of the inventory as an option
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []
        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append('{0} (oi main hand)'.format(item.name))
            elif player.equipment.off_hand == item:
                options.append('{0} (in off hand)'.format(item.name))
            else:
                options.append(item.name)

    menu(con, header, options, inventory_width, screen_width, screen_height)


def main_menu(con, screen_width, screen_height,
              background_image=None,
              background_color=None,
              title='Roguelike Game',
              author='Author',
              option_new='Play a new game',
              option_continue='Continue last game',
              option_quit='Quit',
              additional_options=None):
    """
    Display Main Menu to begin game
    :param libtcod.console con: Console to draw menu on
    :param int screen_width: Screen size
    :param int screen_height: Screen size
    :param background_image: Image to Display
    :param background_color: Color to use if no image present
    :param str title: Game Title text to display
    :param str author: Name to display for the author
    :param str option_new: Text for New Game option
    :param str option_continue: Text for Continue option
    :param str option_quit: Text for Quit option
    :param list additional_options: Other Main-Menu options to display
    """
    if background_image:
        libtcod.image_blit_2x(background_image, 0, 0, 0)
    elif background_color:
        libtcod.console_set_default_background(0, background_color)
        libtcod.console_clear(0)

    libtcod.console_set_default_foreground(0, libtcod.yellow)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                             title)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2), libtcod.BKGND_NONE, libtcod.CENTER,
                             'By: '+author)

    if additional_options is None:
        additional_options = []
    options = [option_new, option_continue, option_quit]
    options.extend(additional_options)
    menu(con, '', options, 24, screen_width, screen_height)


def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    """
    Draw the level-up menu for the Player
    :param libtcod.console con: Console to draw menu on
    :param header:
    :param Entity player: The Entity in the process of levelling up
    :param int menu_width:  Width of the Level-Up Menu in tiles
    :param int screen_width: Screen size
    :param int screen_height: Screen size
    """
    options = ['Constitution (+20 HP from {0})'.format(player.fighter.max_hp),
               'Strength (+1 attach from {0}'.format(player.fighter.power),
               'Agility (+1 defense from {0}'.format(player.fighter.defense)]
    menu(con, header, options, menu_width, screen_width, screen_height)


def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    """
    Draw the Player Info Screen with player details
    :param Entity player: The Entity in the process of levelling up
    :param character_screen_width:  Width of the Player Info Screen in tiles
    :param character_screen_height:  Height of the Player Info Screen in tiles
    :param int screen_width: Screen size
    :param int screen_height: Screen size
    """
    window = libtcod.console_new(character_screen_width, character_screen_height)

    libtcod.console_set_default_foreground(window, libtcod.white)

    libtcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Character Information')
    libtcod.console_print_rect_ex(window, 0, 2, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Level: {0}'.format(player.level.current_level))
    libtcod.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Experience: {0}'.format(player.level.current_xp))
    libtcod.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT,
                                  'Experience to Level: {0}'.format(player.level.experience_to_next_level))
    libtcod.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Maximum HP: {0}'.format(player.fighter.max_hp))
    libtcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Attack: {0}'.format(player.fighter.power))
    libtcod.console_print_rect_ex(window, 0, 8, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Defense: {0}'.format(player.fighter.defense))

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    libtcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)


def message_box(con, header, width, screen_width, screen_height):
    """
    Draw a message box (empty region with no content) to the screen.
    :param libtcod.console con: Console to draw menu on
    :param header:
    :param int width:  Width of the Message Box in tiles
    :param int screen_width: Screen size
    :param int screen_height: Screen size
    """
    menu(con, header, [], width, screen_width, screen_height)
