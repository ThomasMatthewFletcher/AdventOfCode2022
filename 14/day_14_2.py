from dataclasses import dataclass
from typing import Self
import os

def clear():
    os.system('clear')

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Self):
        return Point(
            self.x + other.x,
            self.y + other.y
        )

    def __sub__(self, other: Self):
        return Point(
            self.x - other.x,
            self.y - other.y
        )


class CaveMap:
    walls: set[Point]
    sand: set[Point]
    x_min: int
    x_max: int
    y_min: int
    y_max: int

    def __init__(self):
        self.walls = set()
        self.sand = set()

    def add_wall_line(self, start: Point, end: Point):
        if start.x == end.x:
            # Vertical line
            min_y, max_y = sorted([start.y, end.y])

            for y in range(min_y, max_y+1):
                self._add_wall(Point(start.x, y))

        elif start.y == end.y:
            # Horizontal line
            min_x, max_x = sorted([start.x, end.x])

            for x in range(min_x, max_x+1):
                self._add_wall(Point(x, start.y))

        else:
            raise Exception('Invalid wall line')

    def _add_wall(self, point: Point):
        if not self.walls or point.x < self.x_min:
            self.x_min = point.x

        if not self.walls or point.x > self.x_max:
            self.x_max = point.x

        if not self.walls or point.y < self.y_min:
            self.y_min = point.y

        if not self.walls or point.y > self.y_max:
            self.y_max = point.y

        self.walls.add(point)

    def is_wall(self, point: Point):
        return point in self.walls

    def is_sand(self, point: Point):
        return point in self.sand

    def is_filled(self, point: Point):
        return self.is_wall(point) or self.is_sand(point)

    def add_sand(self, point: Point):
        while point.y <= self.y_max:
            down_point = Point(point.x, point.y + 1)
            down_left_point = Point(point.x - 1, point.y + 1)
            down_right_point = Point(point.x + 1, point.y + 1)

            if not self.is_filled(down_point):
                point = down_point
            elif not self.is_filled(down_left_point):
                point = down_left_point
            elif not self.is_filled(down_right_point):
                point = down_right_point
            else:
                self.sand.add(point)
                return

        self.sand.add(point)


    def __str__(self):
        output = ''

        for y in range(self.y_max + 1):
            for x in range(self.x_min, self.x_max + 1):
                if self.is_wall(Point(x, y)):
                    output += '#'
                elif self.is_sand(Point(x, y)):
                    output += 'o'
                else:
                    output += '.'
            output += '\n'

        return output


def main():
    cave_map = read_cave_map()
    # clear()
    # print(cave_map)

    while not cave_map.is_sand(Point(500, 0)):
        cave_map.add_sand(Point(500, 0))

        # cave_map_str = str(cave_map)
        # clear()
        # print(cave_map_str)

    print('Units of sand:', len(cave_map.sand))

def read_cave_map():
    cave_map = CaveMap()

    with open('14/input.txt', encoding='ascii') as file:
        for line in file:
            wall_line = parse_wall_line(line)

            for i in range(len(wall_line) - 1):
                cave_map.add_wall_line(wall_line[i], wall_line[i+1])

    return cave_map

def parse_wall_line(line: str):
    parts = line.strip().split(' -> ')
    return [parse_point(p) for p in parts]


def parse_point(point_str: str):
    x, y = point_str.split(',')
    return Point(int(x), int(y))


if __name__ == '__main__':
    main()
