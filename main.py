import json
import map
import robot

COLORS = {
    'red': '\033[31m',
    'yellow': '\033[33m',
    'purple': '\033[35m',
    'white': '\033[37m',
    'teal': '\033[36m'
}


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
                picture[y + 1][x + 1] = f'{COLORS["red"]}+{COLORS["white"]}'
            else:
                point = field.get_map()[y][x]
                picture[y + 1][x + 1] = f'{COLORS["yellow"]}{point}{COLORS["white"]}'


def color_text(picture, coord):
    white = COLORS['white']
    teal = COLORS['teal']
    print(f'{teal}" {white}' * (coord[1] - coord[0] + 4))
    for y in range(coord[2], coord[3] + 2):
        print(f'{teal}"{white}',
              *picture[y][coord[0]:coord[1] + 2],
              f'{teal}"{white}')
    print(f'{teal}" {white}' * (coord[1] - coord[0] + 4))


def draw(robot, field):
    purple = COLORS["purple"]
    white = COLORS["white"]
    picture = [[f'{purple}#{white}' for x in range(field.get_width() + 2)]
               for row in range(field.get_height() + 2)]
    update_picture(field, picture)
    coord = calculate_viewzone(field, robot, 3, 3, 3, 3)
    color_text(picture, coord)


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
    field = map.Map(x, y, count)
    center_x = x // 2
    center_y = y // 2
    prepare_field(field, center_x, center_y)
    robot = robot.Robot(center_x, center_y)
    command_handler(robot, field)
    save_logs(robot)
