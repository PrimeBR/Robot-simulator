"""Module containing the map class"""
from random import randint
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

    def __init__(self, x: int, y: int):
        """
        Parameters
        :param x: the width of the map
        :param y: the height of the map
        """
        self.width = x
        self.height = y
        self.map = [[0 for x in range(self.width)]
                    for row in range(self.height)]
        self.barriers_count = 0

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError('Width should be more than 0')
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError('Height should be more than 0')
        self._height = value

    def check_collisions(self, x: int, y: int,
                         off_x: int, off_y: int) -> bool:
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

    def is_full(self):
        """
        Check that there is no place for a barrier on the map

        :return: True if map is full else False
        """

        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == 0:
                    return False
        return True

    def generate_barrier(self, colour: int):
        """
        Generates a new random size barrier

        :param colour: colour(id) of generated barrier
        """

        if self.is_full():
            return None
        x, y, width = 0, 0, 0
        flag = True
        while flag:
            x = randint(0, self.width - 1)
            y = randint(0, self.height - 1)
            width = randint(1, math.ceil(min(self.width, self.height) / 3))
            if not self.check_collisions(x, y, width, width):
                flag = False
        self.barriers_count += 1
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
        self.barriers_count -= 1
        return colour
