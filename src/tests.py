"""
Module contains tests for main functions and methods
from simulator.py, map.py and robot.py modules
"""
import unittest
from map import Map
from robot import Robot
import simulator


class SimulatorTest(unittest.TestCase):

    def test_prepare_field(self):
        """
        First assert to check the function for
        correct processing of the number of barriers.
        Second assert to check that function update map
        """
        field = Map(5, 5)
        simulator.prepare_field(field, 5 // 2, 5 // 2, 30)
        self.assertTrue(field.barriers_count <= 25)

        field = Map(5, 5)
        oldmap = field.map
        simulator.prepare_field(field, 5 // 2, 5 // 2, 30)
        newmap = field.map
        self.assertFalse(oldmap != newmap)

    def test_update_picture(self):
        field = Map(5, 5)
        simulator.prepare_field(field, 5 // 2, 5 // 2, 3)
        picture = [['#' for x in range(5 + 2)]
                   for row in range(5 + 2)]
        simulator.update_picture(field, picture)
        self.assertTrue(' ' in picture[1])

    def test_calculate_viewzone_for_center(self):
        field = Map(7, 7)
        robot = Robot(7 // 2, 7 // 2)
        coord = simulator.calculate_viewzone(field, robot, 3, 3, 3, 3)
        self.assertEqual(coord, (3-3, 3+3, 3-3, 3+3))

    def test_calculate_viewzone_for_corner(self):
        field = Map(7, 7)
        robot = Robot(0, 0)
        coord = simulator.calculate_viewzone(field, robot, 3, 3, 3, 3)
        self.assertEqual(coord, (3-3, 3, 3-3, 3))

    def test_move_robot_1(self):
        """Tests a change in orientation"""
        field = Map(5, 5)
        robot = Robot(5 // 2, 5 // 2)
        old_direction = robot.orientation
        old_coord = (robot.c_x, robot.c_y)
        simulator.move_robot('ROTATE180', robot, field.map)
        new_direction = robot.orientation
        new_coord = (robot.c_x, robot.c_y)
        self.assertNotEqual(new_direction, old_direction)
        self.assertEqual(old_coord, new_coord)

    def test_move_robot_2(self):
        """Tests the position change"""
        field = Map(5, 5)
        robot = Robot(5 // 2, 5 // 2)
        old_coord = (robot.c_x, robot.c_y)
        simulator.move_robot('DOWN', robot, field.map)
        new_coord = (robot.c_x, robot.c_y)
        self.assertNotEqual(old_coord, new_coord)


class MapTest(unittest.TestCase):

    def test_generating_barrier(self):
        field = Map(5, 5)
        old_count = field.barriers_count
        field.generate_barrier(1)
        new_count = field.barriers_count
        self.assertNotEqual(old_count, new_count)

    def test_remove_barrier(self):
        field = Map(5, 5)
        simulator.prepare_field(field, 5 // 2, 5 // 2, 25)
        old_count = field.barriers_count
        field.remove_barrier(0, 0)
        new_count = field.barriers_count
        self.assertNotEqual(old_count, new_count)


class RobotTest(unittest.TestCase):

    def test_update_orientation(self):
        robot = Robot(5 // 2, 5 // 2)
        old_orientation = robot.orientation
        robot.turn_180()
        robot.update_orientation()
        new_orientation = robot.orientation
        self.assertNotEqual(old_orientation, new_orientation)

    def test_step_forward(self):
        robot = Robot(5 // 2, 5 // 2)
        old_coord = (robot.c_x, robot.c_y)
        robot.turn_180()
        robot.update_orientation()
        robot.step_forward()
        new_coord = (robot.c_x, robot.c_y)
        self.assertNotEqual(old_coord, new_coord)
