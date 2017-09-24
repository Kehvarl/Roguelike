import libtcodpy as libtcod
from components.ai import BasicMonster
from components.fighter import Fighter
from map_objects.entity import Entity
from random_utils import random_choice_from_dict
from render_functions import RenderOrder


class MonsterFactory:
    monster_ai = {'basic': BasicMonster,
                  None: BasicMonster}

    @staticmethod
    def get_monster(monster_dict, monster_chances, entities, x, y):
        """
        Randomly Select a Monster from the available monsters, and set it in the map
        :param dictionary monster_dict: dictionary of all available pre-defined monsters
        :param list monster_chances: Monster-generation probabilities for the current level
        :param list entities: Items and Monsters already on the Map.
        :param int x: X position on map
        :param int y: Y position on map
        :return Entity: Monster to be placed in dungeon
        """
        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            return MonsterFactory.get_monster_by_name(monster_dict,
                                                      random_choice_from_dict(monster_chances),
                                                      x, y)

    @staticmethod
    def get_monster_by_name(monster_dict, monster_key, x, y):
        """
        Load a pre-defined Monster and set it at the listed coordinated
        :param dictionary monster_dict: dictionary of all available pre-defined monsters
        :param str monster_key:  Key Value to find Monster from monster_dict
        :param int x: X position on map
        :param int y: Y position on map
        :return Entity: Monster to be placed in dungeon
        """
        monster_choice = monster_dict[monster_key]
        fighter_component = Fighter(hp=monster_choice['hp'],
                                    defense=monster_choice['defense'],
                                    power=monster_choice['power'],
                                    xp=monster_choice['xp'])
        color = getattr(libtcod, monster_choice['color'], libtcod.white)
        ai_component = MonsterFactory.monster_ai[monster_choice.get('ai')](monster_choice.get('ai_action', False),
                                                                           monster_choice.get('action_radius', 10))
        monster = Entity(x, y, monster_choice['symbol'],
                         color,
                         monster_choice['name'],
                         count_value=monster_choice['monster_value'],
                         treasure_value=monster_choice['treasure_value'],
                         blocks=True, render_order=RenderOrder.ACTOR,
                         fighter=fighter_component, ai=ai_component)

        return monster

    @staticmethod
    def build_monster(x, y, monster_symbol='m', monster_color='white',
                      monster_name='generic_monster', monster_ai='basic',
                      ai_action=True, ai_action_radius=10,
                      fighter_hp=1, fighter_defense=0, fighter_power=0, fighter_xp=0,
                      treasure_value=0, count_value=0):
        """
        Create and set a Monster at the specified coordinates
        :param int x: X position on map
        :param int y: Y position on map
        :param str monster_symbol: Monster icon
        :param str monster_color: Color for monster icon
        :param str monster_name: Display Name for monster
        :param str monster_ai: Default AI to use for this monster
        :param int ai_action: Allow Monster to act outside of FOV
        :param int ai_action_radius: Monster will act within this range of the Player
        :param int fighter_hp: Starting Hit Points
        :param int fighter_defense: Defense Combat Value
        :param int fighter_power: Attack Combat Value
        :param int fighter_xp: Experience Points earned for defeating monster
        :param int treasure_value: Treasure dropped by monster
        :param int count_value: Monster's presence count for use in random generation
        :return Entity: Monster to be placed in dungeon
        """
        fighter_component = Fighter(hp=fighter_hp,
                                    defense=fighter_defense,
                                    power=fighter_power,
                                    xp=fighter_xp)
        color = getattr(libtcod, monster_color, libtcod.white)
        ai_component = MonsterFactory.monster_ai[monster_ai](ai_action, ai_action_radius)
        monster = Entity(x, y, monster_symbol,
                         color,
                         monster_name,
                         count_value=count_value,
                         treasure_value=treasure_value,
                         blocks=True, render_order=RenderOrder.ACTOR,
                         fighter=fighter_component, ai=ai_component)

        return monster
