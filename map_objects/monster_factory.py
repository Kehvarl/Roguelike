import libtcodpy as libtcod
from components.ai import BasicMonster
from components.fighter import Fighter
from entity import Entity
from random_utils import random_choice_from_dict
from render_functions import RenderOrder


class MonsterFactory:
    monster_ai = {'basic': BasicMonster,
                  None: BasicMonster}

    @staticmethod
    def get_monster(monster_dict, monster_chances, entities, x, y):
        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            return MonsterFactory.get_monster_by_name(monster_dict,
                                                      random_choice_from_dict(monster_chances),
                                                      x, y)

    @staticmethod
    def get_monster_by_name(monster_dict, monster_name, x, y):
        monster_choice = monster_dict[monster_name]
        fighter_component = Fighter(hp=monster_choice['hp'],
                                    defense=monster_choice['defense'],
                                    power=monster_choice['power'],
                                    xp=monster_choice['xp'])
        color = getattr(libtcod, monster_choice['color'], libtcod.white)
        ai_component = MonsterFactory.monster_ai[monster_choice.get('ai')]()
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
                      fighter_hp=1, fighter_defense=0, fighter_power=0, fighter_xp=0,
                      treasure_value=0, count_value=0):
        fighter_component = Fighter(hp=fighter_hp,
                                    defense=fighter_defense,
                                    power=fighter_power,
                                    xp=fighter_xp)
        color = getattr(libtcod, monster_color, libtcod.white)
        ai_component = MonsterFactory.monster_ai[monster_ai]()
        monster = Entity(x, y, monster_symbol,
                         color,
                         monster_name,
                         count_value=count_value,
                         treasure_value=treasure_value,
                         blocks=True, render_order=RenderOrder.ACTOR,
                         fighter=fighter_component, ai=ai_component)

        return monster

