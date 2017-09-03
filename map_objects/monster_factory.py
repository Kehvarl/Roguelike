import libtcodpy as libtcod

from entity import Entity
from components.ai import BasicMonster
from components.fighter import Fighter
from random_utils import from_dungeon_level, random_choice_from_dict
from render_functions import RenderOrder


class MonsterFactory:

    @staticmethod
    def get_monster(entities, dungeon_level, x, y):
        monster_dict = {
            'orc': {'name': 'Orc',
                    'symbol': 'o',
                    'color': libtcod.desaturated_green,
                    'hp': 20,
                    'defense': 0,
                    'power': 4,
                    'xp': 35},
            'troll': {'name': 'Troll',
                      'symbol': 'T',
                      'color': libtcod.darker_green,
                      'hp': 30,
                      'defense': 2,
                      'power': 8,
                      'xp': 100}
        }

        monster_chances = {'orc': 80,
                           'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]], dungeon_level)}

        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            monster_choice = monster_dict[random_choice_from_dict(monster_chances)]
            fighter_component = Fighter(hp=monster_choice['hp'],
                                        defense=monster_choice['defense'],
                                        power=monster_choice['power'],
                                        xp=monster_choice['xp'])
            ai_component = BasicMonster()
            monster = Entity(x, y, monster_choice['symbol'],
                             monster_choice['color'],
                             monster_choice['name'], blocks=True,
                             render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
            return monster
