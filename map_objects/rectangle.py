class Rect:
    """
    Rectangles used to define Rooms on the map
    """
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

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
        :param Rect other: the other rectangle to test
        :return: True if the two rectangles intersect
        """
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
