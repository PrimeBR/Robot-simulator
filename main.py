import random

shapes = [
        [[1, 1],
         [1, 1]],

        [[0, 2],
         [2, 2]],
    ]


class Map:
    __slots__ = ['width', 'height', 'map', 'barriers']

    def __init__(self, x, y, count):
        self.width = x
        self.height = y
        self.map = [[0 for x in range(self.width)]
                    for row in range(self.height)]
        self.barriers = [shapes[random.randrange(len(shapes))]
                         for i in range(count)]

    def check_collisions(self, x, y, off_x, off_y):
        for cy in range(off_y):
            for cx in range(off_x):
                try:
                    if self.map[y + cy][x + cx] > 0:
                        return True
                except IndexError:
                    return True

        return False

    def generate_barrier(self, barrier):
        x = random.randint(0, self.width-1)
        y = random.randint(0, self.height-1)
        off_x = len(barrier[0])
        off_y = len(barrier)
        if self.check_collisions(x, y, off_x, off_y):
            self.generate_barrier(barrier)
            return
        for cy in range(off_y):
            for cx in range(off_x):
                print(y,cy, x,cx)
                self.map[y + cy][x + cx] = barrier[cy][cx]


if __name__ == '__main__':
    x = int(input('Enter the X: '))
    y = int(input('Enter the Y: '))
    count = int(input('Enter the number of barriers: '))
    field = Map(x, y, count)
    for index, item in enumerate(field.barriers):
        print(item)
        field.generate_barrier(item)
    for i in enumerate(field.map):
        print(i)
