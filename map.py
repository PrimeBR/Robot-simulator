"""Module containing the map class"""
import random
import math


class Map:
    """
    A class used to represent map

    Attributes:
        width : int
            the width of the map
        height : int
            the height of the map
        map : list
            a list that stores information about each point on the map
        barriers_count : int
            number of barriers on the map
    """

    __slots__ = ('width', 'height', 'map', 'barriers_count')

    def __init__(self, x: int, y: int, count: int):
        """
        Parameters
        :param x: the width of the map
        :param y: the height of the map
        :param count: number of barriers on the map
        """
        self.width = x
        self.height = y
        self.map = [[0 for x in range(self.width)]
                    for row in range(self.height)]
        self.barriers_count = count

    def get_width(self) -> int:
        """Return the width of the map"""

        return self.width

    def get_height(self) -> int:
        """Return the height of the map"""

        return self.height

    def get_map(self) -> list:
        """Return the map"""

        return self.map

    def check_collisions(self, x: int, y: int, off_x: int, off_y: int) -> bool:
        """
        Checks whether there are collisions in a particular zone

        :param x: coordinate of the upper-left corner of the zone by X
        :param y: coordinate of the upper-left corner of the zone by Y
        :param off_x: width of the zone to be checked
        :param off_y: height of the zone to be checked
        :return: True if a collisions was found else False
        """

        for cy in range(off_y):
            for cx in range(off_x):
                try:
                    if self.map[y + cy][x + cx] > 0:
                        return True
                except IndexError:
                    return True

        return False

    def free_point(self, x: int, y: int) -> bool:
        """
        Check if the point is free

        :param x: X coordinate of the point
        :param y: Y coordinate of the point
        :return: True if point is free else False
        """

        return True if self.map[y][x] == 0 else False

    def generate_barrier(self, colour: int):
        """
        Generates a new random size barrier

        :param colour: colour(id) of generated barrier
        :return: None if collision was found or
                hit limit on the depth of recursion
        """

        try:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
        except RecursionError:
            return None
        width = random.randint(1, math.ceil(min(self.width, self.height) / 3))
        if self.check_collisions(x, y, width, width):
            self.generate_barrier(colour)
            return None
        for cy in range(width):
            for cx in range(width):
                self.map[y + cy][x + cx] = colour

    def remove_barrier(self, x: int, y: int) -> int:
        """
        Delete the barrier to which the transmitted point belongs.

        :param x: coordinate of point by X
        :param y: coordinate of point by Y
        :return: colour(id) of removed barrier
        """

        colour = self.map[y][x]
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == colour:
                    self.map[y][x] = 0
        return colour
