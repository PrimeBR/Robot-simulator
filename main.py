"""
The module contains simulator functions for correct data entry,
interaction between the robot and the field, and display,
as well as displaying the results of work.
"""
import json
from map import Map
from robot import Robot
from typing import Tuple


COLORS = {
    'red': '\033[31m',
    'yellow': '\033[33m',
    'purple': '\033[35m',
    'white': '\033[37m',
    'teal': '\033[36m'
}


def calculate_viewzone(field: Map, robot: Robot, x_1: int = 3,
                       x_2: int = 3, y_1: int = 3, y_2: int = 3) -> Tuple:
    """
    Calculates the visible area of the robot field

    :param field: the field where the visible zone is calculated
    :param robot: the robot for which the viewing area is calculated
    :param x_1: X coordinate of the upper-left corner of view zone
    :param x_2: X coordinate of the lower-right corner of view zone
    :param y_1: Y coordinate of the upper-left corner of view zone
    :param y_2: Y coordinate of the lower-right corner of view zone
    :return: tuple of the above points
    """

    while robot.c_x + x_2 > field.width:
        x_2 -= 1
    while robot.c_x - x_1 < 0:
        x_1 -= 1
    while robot.c_y + y_2 > field.height:
        y_2 -= 1
    while robot.c_y - y_1 < 0:
        y_1 -= 1
    x_1 = robot.c_x - x_1
    x_2 = robot.c_x + x_2
    y_1 = robot.c_y - y_1
    y_2 = robot.c_y + y_2
    return x_1, x_2, y_1, y_2


def update_picture(field: Map, picture: list):
    """
    Updates a human readable field image

    :param field: the field that is used to update the field image
    :param picture: the image that you want to update
    """

    for y in range(field.height):
        for x in range(field.width):
            if field.map[y][x] == 0:
                picture[y + 1][x + 1] = ' '
            elif type(field.map[y][x]) is int:
                picture[y + 1][x + 1] = f'{COLORS["red"]}+{COLORS["white"]}'
            else:
                point = field.map[y][x]
                picture[y + 1][x + 1] = f'{COLORS["yellow"]}{point}{COLORS["white"]}'


def color_picture(picture: list, coord: Tuple):
    """
    Displays a color image of the visible area in the terminal output

    :param picture: images for which colors are added
    :param coord: coordinates of view zone
    """

    white = COLORS['white']
    teal = COLORS['teal']
    print(f'{teal}" {white}' * (coord[1] - coord[0] + 4))
    for y in range(coord[2], coord[3] + 2):
        print(f'{teal}"{white}',
              *picture[y][coord[0]:coord[1] + 2],
              f'{teal}"{white}')
    print(f'{teal}" {white}' * (coord[1] - coord[0] + 4))


def draw(robot: Robot, field: Map):
    """
    Displays the current location of
     the robot and the visible area of the field

    :param robot: the robot whose position you want to display
    :param field: the field where the robot moves
    """

    purple = COLORS["purple"]
    white = COLORS["white"]
    picture = [[f'{purple}#{white}' for x in range(field.width + 2)]
               for row in range(field.height + 2)]
    update_picture(field, picture)
    coord = calculate_viewzone(field, robot)
    color_picture(picture, coord)


def move_robot(command: str, robot: Robot, map: list):
    """
    Moves the robot around the map in
     accordance with the received command

    :param command: the command you want to execute
    :param robot: the robot for which the command is passed
    :param map: the field where the robot moves
    """

    flag = False
    while robot.orientation != command:
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


def read_param(param_name: str) -> int:
    """
    Reads and checks for correctness the field size
     and the number of barriers

    :param param_name: name of the parameter to be read and checked for
    :return: returns the reading result for param_name
    """

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


def prepare_field(field: Map, x: int, y: int, count: int):
    """
    Prepares the field for placing the robot on it

    :param field: the field that you want to prepare
    :param x: the X-coordinate of the point
              that should be free for the robot
    :param y: the Y-coordinate of the point that
              should be free for the robot
    :param count: the count of barriers
    """

    for index in range(1, count + 1):
        field.generate_barrier(index)
    while not field.free_point(x=x, y=y):
        field.remove_barrier(x=x, y=y)


def command_handler(robot: Robot, field: Map):
    """
    Reads, checks, and processes input commands from the terminal

    :param robot: the robot for which commands are sent
    :param field: the field where the robot moves
    """

    commands = (
        'UP',
        'DOWN',
        'LEFT',
        'RIGHT',
        'ROTATE90',
        'ROTATE180',
        'QUIT'
    )
    while True:
        x = robot.c_x
        y = robot.c_y
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


def save_logs(robot: Robot):
    """
    Prompts the user to record the robot's traces in a json file

    :param robot: robot whose traces will be recorded
    """

    answer = ''
    while answer not in ('Y', 'N'):
        answer = input('Do you want to save robot traces(Y/N)?: ').upper()
    if answer == 'Y':
        with open('traces.json', 'w') as file:
            json.dump(robot.trace, file)
    else:
        return None


def start():
    """Run robot simulator"""
    x = read_param('X')
    y = read_param('Y')
    count = read_param('number of barriers')
    field = Map(x, y)
    center_x = x // 2
    center_y = y // 2
    prepare_field(field, center_x, center_y, count)
    robot = Robot(center_x, center_y)
    command_handler(robot, field)
    save_logs(robot)


if __name__ == '__main__':
    start()
