import libtcodpy as libtcod
from components.spawner import MonsterSpawner
from map_objects.entity import Entity
from random_utils import random_choice_from_dict
from render_functions import RenderOrder


class SpawnerFactory:
    @staticmethod
    def get_monster_spawner(monster_dict, monster_chances, entities, x, y, room):
        """
        Randomly Select a Monster from the available monsters, and set it in the map
        :param dictionary monster_dict: dictionary of all available pre-defined monsters
        :param list monster_chances: Monster-generation probabilities for the current level
        :param list entities: Items and Monsters already on the Map.
        :param Rect room: room
        :param int x: X position on map
        :param int y: Y position on map
        :return Entity: Monster to be placed in dungeon
        """
        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            return SpawnerFactory.get_monster_spawner_by_name(monster_dict,
                                                              random_choice_from_dict(monster_chances),
                                                              x, y, room)

    @staticmethod
    def get_monster_spawner_by_name(monster_dict, monster_key, x, y, room):
        """
        Load a pre-defined Monster and set it at the listed coordinated
        :param dictionary monster_dict: dictionary of all available pre-defined monsters
        :param str monster_key:  Key Value to find Monster from monster_dict
        :param int x: X position on map
        :param int y: Y position on map
        :param Rect room: room
        :return Entity: Monster to be placed in dungeon
        """
        monster_choice = monster_dict[monster_key]
        spawner_component = MonsterSpawner(room, monster_choice['symbol'],
                                           monster_choice['color'], monster_choice['name'],
                                           monster_choice.get('ai'), monster_choice.get('ai_action', False),
                                           monster_choice.get('action_radius', 10),
                                           monster_choice['hp'], monster_choice['defense'],
                                           monster_choice['power'], monster_choice['xp'],
                                           monster_choice['treasure_value'],
                                           monster_choice['monster_value'])

        name = '{0} Spawner'.format(monster_choice['name'])
        spawner = Entity(x, y, '.', libtcod.white, name,
                         blocks=False, render_order=RenderOrder.ITEM,
                         spawner=spawner_component)

        return spawner
