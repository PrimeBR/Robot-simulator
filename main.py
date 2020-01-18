import random
import math


class Map:
    __slots__ = ('width', 'height', 'map', 'barriers', 'barriers_count')

    def __init__(self, x, y, count):
        self.width = x
        self.height = y
        self.map = [[0 for x in range(self.width)]
                    for row in range(self.height)]
        self.barriers_count = count
        self.barriers = {}

    def check_collisions(self, x, y, off_x, off_y):
        for cy in range(off_y):
            for cx in range(off_x):
                try:
                    if self.map[y + cy][x + cx] > 0:
                        return True
                except IndexError:
                    return True

        return False

    def free_point(self, x, y):
        return True if self.map[y][x] == 0 else False

    def generate_barrier(self, colour):
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

    def remove_barrier(self, x, y):
        colour = self.map[x][y]
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == colour:
                    self.map[y][x] = 0
        return colour


class Robot:
    __slots__ = ('view', 'orientation', 'directions', 'c_y', 'c_x', 'angle', 'step')

    def __init__(self, center_x, center_y):
        self.c_x = center_x
        self.c_y = center_y
        self.orientation = 'UP'
        self.view = '^'
        self.directions = {'UP': [-630, -270, 90, 450],
                           'DOWN': [-90, -450, 270, 630],
                           'RIGHT': [-720, -360, 0, 360, 720],
                           'LEFT': [-540, -180, 180, 540]}
        self.angle = 90
        self.step = 1

    def get_direction(self):
        return self.orientation

    def get_x(self):
        return self.c_x

    def get_y(self):
        return self.c_y

    def turn_right(self):
        self.angle -= 90
        self.check_angle()

    def turn_180(self):
        self.angle -= 180
        self.check_angle()

    def check_angle(self):
        if self.angle >= 360:
            self.angle -= 360
        elif self.angle <= -360:
            self.angle += 360

    def handling_turns(self, command):
        if command == 'ROTATE90':
            self.turn_right()
            self.orientation = command
        elif command == 'ROTATE180':
            self.turn_180()
            self.orientation = command
        else:
            self.turn_right()
            self.update_orientation()

    def step_forward(self):
        if self.orientation == 'UP':
            self.c_y -= self.step
            self.view = '^'
        elif self.orientation == 'DOWN':
            self.c_y += self.step
            self.view = 'v'
        elif self.orientation == 'LEFT':
            self.c_x -= self.step
            self.view = '<'
        elif self.orientation == 'RIGHT':
            self.c_x += self.step
            self.view = '>'
        self.step = 1

    def update_orientation(self):
        if self.orientation == 'ROTATE90' or self.orientation == 'ROTATE180':
            self.step = 0
        if self.angle in self.directions['LEFT']:
            self.orientation = 'LEFT'
            return 0, -self.step
        elif self.angle in self.directions['RIGHT']:
            self.orientation = 'RIGHT'
            return 0, self.step
        elif self.angle in self.directions['UP']:
            self.orientation = 'UP'
            return -self.step, 0
        elif self.angle in self.directions['DOWN']:
            self.orientation = 'DOWN'
            return self.step, 0
        return 0, 0

    def check_collisions(self, map, off_x, off_y):
        if off_x == 0 and off_y == 0:
            return False
        try:
            if self.c_y + off_y < 0:
                print('Oops...We hit a border. Try again.')
                return True
            elif self.c_x + off_x < 0:
                print('Oops...We hit a border. Try again.')
                return True
            elif map[self.c_y + off_y][self.c_x + off_x] > 0:
                print('Oops...We hit a barrier. Try again.')
                return True
        except IndexError:
            print('Oops...We hit a border. Try again.')
            return True
        return False


def move_robot(command, robot, map):
    while robot.get_direction() != command:
        robot.handling_turns(command)
        # robot.turn_right()
        # robot.update_orientation()
    off_y, off_x = robot.update_orientation()
    if not robot.check_collisions(map, off_x, off_y):
        robot.step_forward()


if __name__ == '__main__':
    x = int(input('Enter the X: '))
    y = int(input('Enter the Y: '))
    count = int(input('Enter the number of barriers: '))
    field = Map(x, y, count)
    for index in range(1, field.barriers_count+1):
        field.generate_barrier(index)
    center_x = x // 2
    center_y = x // 2
    while not field.free_point(x=center_x, y=center_y):
        colour = field.remove_barrier(x=center_x, y=center_y)
        field.generate_barrier(colour)
    robot = Robot(center_x, center_y)
    command = ''
    while True:
        x = robot.c_x
        y = robot.c_y
        field.map[y][x] = robot.view
        for i in enumerate(field.map):
            print(*i[1])
        command = input('Enter command: ').strip().upper()
        move_robot(command, robot, field.map)
        field.map[y][x] = 0
