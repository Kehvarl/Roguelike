import libtcodpy as libtcod
from game_messages import Message
from game_states import GameStates
from map_objects.entity import Entity
from render_functions import RenderOrder


def kill_player(player):
    player.char = '%'
    player.color = libtcod.dark_red

    return Message('You Died!', libtcod.red), GameStates.PLAYER_DEAD


def kill_monster(monster):
    """
    The Death of a Monster
    :param Entity monster: the monster being killed
    :return Message: Notification of Killed Monster
    """
    death_message = Message('{0} is dead!'.format(monster.name.capitalize()), libtcod.orange)

    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.count_value = 0
    monster.treasure_value = 0
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE

    return death_message
