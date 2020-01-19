import random
import math
import json

class Map:
    __slots__ = ('width', 'height', 'map', 'barriers', 'barriers_count')

    def __init__(self, x, y, count):
        self.width = x
        self.height = y
        self.map = [[0 for x in range(self.width)]
                    for row in range(self.height)]
        self.barriers_count = count

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_map(self):
        return self.map

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
        colour = self.map[y][x]
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == colour:
                    self.map[y][x] = 0
        return colour


class Robot:
    __slots__ = ('view',
                 'orientation',
                 'directions',
                 'c_y',
                 'c_x',
                 'angle',
                 'step',
                 'trace')

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
        self.trace = ''

    def get_direction(self):
        return self.orientation

    def get_x(self):
        return self.c_x

    def get_y(self):
        return self.c_y

    def get_trace(self):
        return self.trace

    def turn_90(self):
        self.angle -= 90

    def turn_180(self):
        self.angle -= 180

    def check_angle(self):
        if self.angle >= 360:
            self.angle -= 360
        elif self.angle <= -360:
            self.angle += 360

    def handling_command(self, command):
        if command == 'ROTATE90':
            self.turn_90()
            self.update_orientation(rotation=command)

        elif command == 'ROTATE180':
            self.turn_180()
            self.update_orientation(rotation=command)
            # self.orientation = command
        else:
            self.turn_90()
            self.update_orientation()
        self.check_angle()

    def step_forward(self):
        if self.orientation == 'UP':
            self.c_y -= self.step
        elif self.orientation == 'DOWN':
            self.c_y += self.step
        elif self.orientation == 'LEFT':
            self.c_x -= self.step
        elif self.orientation == 'RIGHT':
            self.c_x += self.step
        self.step = 1

    def update_orientation(self, rotation=None):
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

    def print_state(self, off_x, off_y):
        if off_x == 0 and off_y == 0:
            state = f'Robot turned {self.orientation}'
        else:
            state = f'Robot direction: {self.orientation}\n'\
                    f'Robot arrived to [{self.c_x + off_x}, {self.c_y + off_y}]' \
                    f' from [{self.c_x}, {self.c_y}]'
        self.trace += f'{state}\n'
        print(state)


def calculate_viewzone(field, robot, x_1, x_2, y_1, y_2):
    while robot.get_x() + x_2 > field.get_width():
        x_2 -= 1
    while robot.get_x() - x_1 < 0:
        x_1 -= 1
    while robot.get_y() + y_2 > field.get_height():
        y_2 -= 1
    while robot.get_y() - y_1 < 0:
        y_1 -= 1
    x_1 = robot.get_x() - x_1
    x_2 = robot.get_x() + x_2
    y_1 = robot.get_y() - y_1
    y_2 = robot.get_y() + y_2
    return x_1, x_2, y_1, y_2


def update_picture(field, picture):
    for y in range(field.get_height()):
        for x in range(field.get_width()):
            if field.get_map()[y][x] == 0:
                picture[y + 1][x + 1] = ' '
            elif type(field.get_map()[y][x]) is int:
                picture[y + 1][x + 1] = '\033[31m+\033[37m'
            else:
                picture[y + 1][x + 1] = f'\033[33m{field.get_map()[y][x]}\033[37m'


def draw(robot, field):
    picture = [['\033[35m#\033[37m' for x in range(field.get_width() + 2)]
               for row in range(field.get_height() + 2)]
    update_picture(field, picture)
    coord = calculate_viewzone(field, robot, 3, 3, 3, 3)
    print('\033[36m" \033[37m' * (coord[1] - coord[0] + 4))
    for y in range(coord[2], coord[3] + 2):
        print('\033[36m"\033[37m',
              *picture[y][coord[0]:coord[1] + 2],
              '\033[36m"\033[37m')
    print('\033[36m" \033[37m' * (coord[1] - coord[0] + 4))


def move_robot(command, robot, map):
    flag = False
    while robot.get_direction() != command:
        robot.handling_command(command)
        if command.find('ROTATE') == -1:
            robot.print_state(0, 0)
        else:
            flag = True
        if flag:
            break
    off_y, off_x = robot.update_orientation()
    if not robot.check_collisions(map, off_x, off_y):
        robot.print_state(off_x, off_y)
        robot.step_forward()


def read_param(param_name):
    while True:
        try:
            param = int(input(f'Enter the {param_name}: ').strip())
            while param <= 0 and (param_name == 'X' or param_name == 'Y'):
                print('Error! Size of field must be'
                      ' positive and greater than zero.')
                param = int(input(f'Enter the {param_name}: ').strip())
            while param < 0:
                print('Error! Count of barriers must be positive')
                param = int(input(f'Enter the {param_name}: ').strip())
            return param
        except ValueError:
            print('Error! Enter only an integer value.')


def prepare_field(field, x, y):
    if field.barriers_count > field.get_height() * field.get_width():
        field.barriers_count = field.get_width() * field.get_height()
    for index in range(1, field.barriers_count + 1):
        field.generate_barrier(index)
    while not field.free_point(x=x, y=y):
        field.remove_barrier(x=x, y=y)


def command_handler(robot, field):
    commands = ('UP', 'DOWN', 'LEFT', 'RIGHT', 'ROTATE90', 'ROTATE180', 'QUIT')
    while True:
        x = robot.get_x()
        y = robot.get_y()
        field.map[y][x] = robot.view
        draw(robot, field)
        command = input('Enter command: ').strip().upper()
        while command not in commands:
            print("Unknown command. Try to use:\n"
                  "'UP', 'DOWN', 'LEFT', 'RIGHT',"
                  " 'ROTATE90', 'ROTATE180', 'QUIT'")
            command = input('Enter command: ').strip().upper()
        if command == 'QUIT':
            field.map[y][x] = 0
            return None
        move_robot(command, robot, field.map)
        field.map[y][x] = 0


def save_logs(robot):
    answer = ''
    while answer not in ['Y', 'N']:
        answer = input('Do you want to save robot traces(Y/N)?: ').upper()
    if answer == 'Y':
        with open('traces.json', 'w') as file:
            json.dump(robot.get_trace(), file)
    else:
        return None


if __name__ == '__main__':
    x = read_param('X')
    y = read_param('Y')
    count = read_param('number of barriers')
    field = Map(x, y, count)
    center_x = x // 2
    center_y = y // 2
    prepare_field(field, center_x, center_y)
    robot = Robot(center_x, center_y)
    command_handler(robot, field)
    save_logs(robot)
