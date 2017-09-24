from random import randint


class Room:
    """
    Rectangles used to define Rooms on the map
    """
    def __init__(self, x, y, w, h, monster_limit=0):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        self.monster_limit = monster_limit

    def center(self):
        """
        Return the center point of the current rectangle
        :return int, int: x-position, y-position of rectangle center
        """
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    def intersect(self, other):
        """
        Test if another rectangle intersects this one at any point
        :param Room other: the other rectangle to test
        :return: True if the two rectangles intersect
        """
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

    def random_point(self):
        """
        Return a random point within the current rectangle
        :return int, int: x-position, y-position within the rectangle
        """
        x = randint(self.x1 + 1, self.x2 - 1)
        y = randint(self.y1 + 1, self.y2 - 1)
        return x, y

    def monster_limit_reached(self, entities):
        """
        Check Room to see if it can support more monsters
        :param dictionary entities:  Objects on the map
        :return boolean: Number of Monsters in Room is at room Limit
        """
        monster_count = sum([entity.count_value for entity in entities
                             if self.x1 < entity.x < self.x2 and
                             self.y1 < entity.y < self.y2])
        return monster_count < self.monster_limit
