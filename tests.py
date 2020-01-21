"""
Module contains tests for main functions and methods
from main.py, map.py and robot.py modules
"""
import unittest
from map import Map
from robot import Robot
import main


class PrepareFieldTest(unittest.TestCase):

    def test_for_barriers_count(self):
        field = Map(5, 5)
        main.prepare_field(field, 5 // 2, 5 // 2, 30)
        self.assertTrue(field.barriers_count <= 25)

    def test_updated_field(self):
        field = Map(5, 5)
        oldmap = field.map
        main.prepare_field(field, 5 // 2, 5 // 2, 30)
        newmap = field.map
        self.assertFalse(oldmap != newmap)


class UpdatePictureTest(unittest.TestCase):

    def test_correct_work(self):
        field = Map(5, 5)
        main.prepare_field(field, 5 // 2,  5 // 2, 3)
        picture = [['#' for x in range(5 + 2)]
                   for row in range(5 + 2)]
        main.update_picture(field, picture)
        self.assertTrue(' ' in picture[1])


class CalculateViewZoneTest(unittest.TestCase):

    def test_calculating_for_center(self):
        field = Map(7, 7)
        robot = Robot(7 // 2, 7 // 2)
        coord = main.calculate_viewzone(field, robot, 3, 3, 3, 3)
        self.assertEqual(coord, (3-3, 3+3, 3-3, 3+3))

    def test_calculating_for_corner(self):
        field = Map(7, 7)
        robot = Robot(0, 0)
        coord = main.calculate_viewzone(field, robot, 3, 3, 3, 3)
        self.assertEqual(coord, (3-3, 3, 3-3, 3))


class MoveRobotTest(unittest.TestCase):

    def test_change_orientation(self):
        field = Map(5, 5)
        robot = Robot(5 // 2, 5 // 2)
        old_direction = robot.orientation
        old_coord = (robot.c_x, robot.c_y)
        main.move_robot('ROTATE180', robot, field.map)
        new_direction = robot.orientation
        new_coord = (robot.c_x, robot.c_y)
        self.assertNotEqual(new_direction, old_direction)
        self.assertEqual(old_coord, new_coord)

    def test_change_movement(self):
        field = Map(5, 5)
        robot = Robot(5 // 2, 5 // 2)
        old_coord = (robot.c_x, robot.c_y)
        main.move_robot('DOWN', robot, field.map)
        new_coord = (robot.c_x, robot.c_y)
        self.assertNotEqual(old_coord, new_coord)
