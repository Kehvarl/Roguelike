from map_objects.monster_factory import MonsterFactory
from map_objects.map_room import Room
from map_objects.entity import Entity


class MonsterSpawner:
    def __init__(self, room,
                 monster_symbol='m', monster_color='white',
                 monster_name='generic_monster', monster_ai='basic',
                 ai_action=True, ai_action_radius=10,
                 fighter_hp=1, fighter_defense=0, fighter_power=0, fighter_xp=0,
                 treasure_value=0, count_value=0, cooldown=50, spawn_radius=20):
        """
        Create and set a Monster at the specified coordinates
        :param Room room: containing the spawner
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
        :param int cooldown: Number of turns that must elapse before Spawner can trigger again
        :param int spawn_radius: Only spawn if Player within this range
        """
        self.room = room
        self.monster_symbol = monster_symbol
        self.monster_color = monster_color
        self.monster_name = monster_name
        self.monster_ai = monster_ai
        self.ai_action = ai_action
        self.ai_action_radius = ai_action_radius
        self.fighter_hp = fighter_hp
        self.fighter_defense = fighter_defense
        self.fighter_power = fighter_power
        self.fighter_xp = fighter_xp
        self.treasure_value = treasure_value
        self.count_value = count_value
        self.spawner_cooldown = cooldown
        self.spawn_radius = spawn_radius
        self.spawner_cooldown_level = 0

    def spawn(self, entities, player):
        """
        Attempt to trigger spawner
        :param dict entities:
        :param Entity player:
        :return Entity: Monster to be placed in dungeon
        """
        if self.can_spawn(entities, player):
            x, y, = self.room.random_point()
            return MonsterFactory.build_monster(x, y,
                                                self.monster_symbol, self.monster_color,
                                                self.monster_name, self.monster_ai,
                                                self.ai_action, self.ai_action_radius,
                                                self.fighter_hp, self.fighter_defense,
                                                self.fighter_power, self.fighter_xp,
                                                self.treasure_value, self.count_value)

    def can_spawn(self, entities, player):
        """
        Current Spawner is not in cooldown period and Room is not at monster limit
        :param dict entities:
        :param Entity player:
        :return boolean: True if Spawning is allowed
        """
        if self.spawner_cooldown_level > 0:
            self.spawner_cooldown_level -= 1
            return False
        else:
            if player.distance_to(self.owner) <= self.spawn_radius:
                self.spawner_cooldown_level = self.spawner_cooldown
                return self.room.monster_limit_reached(entities)
