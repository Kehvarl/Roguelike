import libtcodpy as libtcod


class BasicMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        """
        Perform the AI actions on its turn
        :param Entity target:
        :param fov_map:
        :param GameMap game_map:
        :param List entities:
        """
        results = []

        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if monster.distance_to(target) > 2:
                monster.move_astar(target, entities, game_map)
                # monster.move_towards(target.x, target.y, game_map, entities)
            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results
