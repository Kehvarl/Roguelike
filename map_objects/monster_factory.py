import libtcodpy as libtcod

from entity import Entity
from components.ai import BasicMonster
from components.fighter import Fighter
from random_utils import from_dungeon_level, random_choice_from_dict
from render_functions import RenderOrder


class MonsterFactory:
    @staticmethod
    def get_monster(monster_dict, entities, dungeon_level, x, y):

        monster_chances = {'kobold': 75,
                           'orc': from_dungeon_level([[25, 1], [45, 3], [65, 5]], dungeon_level),
                           'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]], dungeon_level)}

        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            monster_choice = monster_dict[random_choice_from_dict(monster_chances)]
            fighter_component = Fighter(hp=monster_choice['hp'],
                                        defense=monster_choice['defense'],
                                        power=monster_choice['power'],
                                        xp=monster_choice['xp'])
            color = getattr(libtcod, monster_choice['color'], libtcod.white)
            if monster_choice['ai'] == 'basic':
                ai_component = BasicMonster()
            else:
                ai_component = BasicMonster()
            monster = Entity(x, y, monster_choice['symbol'],
                             color,
                             monster_choice['name'],
                             monster_value=monster_choice['monster_value'],
                             blocks=True, render_order=RenderOrder.ACTOR,
                             fighter=fighter_component, ai=ai_component)
            return monster
