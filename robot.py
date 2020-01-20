"""Module containing the robot class"""
from typing import Tuple


class Robot:
    """
    A class used to represent an Robot

    Attributes:
        view : str
            the image of the robot
        orientation : str
            the current direction of the robot
        directions : dict
            contains the directions and angles that correspond to them
        c_y : int
            current position of the robot by Y
        c_x : int
            current position of the robot by X
        angle : int
            the current value of the angle
        step : int
            the step size of the robot
        trace : str
            contains logs of robot movements
    """
    __slots__ = ('view',
                 'orientation',
                 'directions',
                 'c_y',
                 'c_x',
                 'angle',
                 'step',
                 'trace')

    def __init__(self, center_x: int, center_y: int):
        """
        Parameters
        :param center_x: center coordinate by X
        :param center_y: center coordinate by Y
        """

        self.c_x = center_x
        self.c_y = center_y
        self.orientation = 'UP'
        self.view = '^'
        self.directions = {
            'UP': [-630, -270, 90, 450],
            'DOWN': [-90, -450, 270, 630],
            'RIGHT': [-720, -360, 0, 360, 720],
            'LEFT': [-540, -180, 180, 540]
        }
        self.angle = 90
        self.step = 1
        self.trace = ''

    def get_direction(self) -> str:
        """Return the current direction of robot"""

        return self.orientation

    def get_x(self) -> int:
        """Return the current position of the robot by X"""

        return self.c_x

    def get_y(self) -> int:
        """Return the current position of the robot by Y"""

        return self.c_y

    def get_trace(self) -> str:
        """Return current logs of robot movements"""

        return self.trace

    def turn_90(self):
        """Rotates the robot 90 degrees"""

        self.angle -= 90

    def turn_180(self):
        """Rotates the robot 180 degrees"""

        self.angle -= 180

    def check_angle(self):
        """
        Reduces the robot's angle by 360
         if it becomes more or less than 360 degrees
         """

        if self.angle >= 360:
            self.angle -= 360
        elif self.angle <= -360:
            self.angle += 360

    def handling_command(self, command: str):
        """
        Processes the command and
         performs the appropriate actions for the command

        :param command: the command to be processed
        """

        if command == 'ROTATE90':
            self.turn_90()
            self.update_orientation(rotation=command)
        elif command == 'ROTATE180':
            self.turn_180()
            self.update_orientation(rotation=command)
        else:
            self.turn_90()
            self.update_orientation()
        self.check_angle()

    def step_forward(self):
        """Forces the robot to take a step in a certain direction"""

        if self.orientation == 'UP':
            self.c_y -= self.step
        elif self.orientation == 'DOWN':
            self.c_y += self.step
        elif self.orientation == 'LEFT':
            self.c_x -= self.step
        elif self.orientation == 'RIGHT':
            self.c_x += self.step
        self.step = 1

    def update_orientation(self, rotation: str = None) -> Tuple[int, int]:
        """
        Updates the robot's direction and changes its image accordingly

        :param rotation:
            flag that controls whether
             the robot was given a rotation command or not.
             (default is None)
        :return:
            Returns a pair of points
            that are responsible for the offset for the robot's offset
        """

        if rotation:
            self.step = 0
        if self.angle in self.directions['LEFT']:
            self.orientation = 'LEFT'
            self.view = '<'
            return 0, -self.step
        elif self.angle in self.directions['RIGHT']:
            self.orientation = 'RIGHT'
            self.view = '>'
            return 0, self.step
        elif self.angle in self.directions['UP']:
            self.orientation = 'UP'
            self.view = '^'
            return -self.step, 0
        elif self.angle in self.directions['DOWN']:
            self.orientation = 'DOWN'
            self.view = 'v'
            return self.step, 0
        return 0, 0

    def check_collisions(self, field: list, off_x: int, off_y: int) -> bool:
        """
        Checks whether the robot has encountered an obstacle or not.

        :param field: field on which the robot rides
        :param off_x: robot's offset by X
        :param off_y: robot's offset by Y
        :return: True if a collisions was found else False
        """

        if off_x == 0 and off_y == 0:
            return False
        try:
            if self.c_y + off_y < 0:
                print('Oops...We hit a border. Try again.')
                return True
            elif self.c_x + off_x < 0:
                print('Oops...We hit a border. Try again.')
                return True
            elif field[self.c_y + off_y][self.c_x + off_x] > 0:
                print('Oops...We hit a barrier. Try again.')
                return True
        except IndexError:
            print('Oops...We hit a border. Try again.')
            return True
        return False

    def print_state(self, off_x: int, off_y: int):
        """
        Displays the robot status to the user after
        executing the command and adds traces
        
        :param off_x: robot's offset by X
        :param off_y: robot's offset by Y
        """

        if off_x == 0 and off_y == 0:
            state = f'Robot turned {self.orientation}'
        else:
            shifted_x = self.c_x + off_x
            shifted_y = self.c_y + off_y
            state = f'Robot direction: {self.orientation}\n'\
                    f'Robot arrived to [{shifted_x}, {shifted_y}]' \
                    f' from [{self.c_x}, {self.c_y}]'
        self.trace += f'{state}\n'
        print(state)
