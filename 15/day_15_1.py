from typing import NamedTuple, Self
import re

class Point(NamedTuple):
    x: int
    y: int

    @classmethod
    def manhatten_dist(cls, a: Self, b: Self) -> int:
        return abs(b.x - a.x) + abs(b.y - a.y)


class Sensor:
    pos: Point
    closest_beacon: Point
    range: int

    def __init__(self, pos: Point, closest_beacon: Point):
        self.pos = pos
        self.closest_beacon = closest_beacon
        self.range = Point.manhatten_dist(pos, closest_beacon)

    def range_at_y(self, y: int) -> tuple[int, int] | None:
        y_offset = abs(self.pos.y - y)

        x_range = self.range - y_offset

        if x_range < 0:
            return None

        return (self.pos.x - x_range, self.pos.x + x_range)


def main():
    sensors = read_sensors()
    beacon_positions = {sensor.closest_beacon for sensor in sensors}

    not_beacon_points: set[Point] = set()

    y = 2000000

    for sensor in sensors:
        x_range = sensor.range_at_y(y)

        if x_range:
            for x in range(x_range[0], x_range[1] + 1):
                point = Point(x, y)

                if point not in beacon_positions:
                    not_beacon_points.add(point)

    print('Not beacon points:', len(not_beacon_points))


def read_sensors() -> list[Sensor]:
    with open('15/input.txt', encoding='ascii') as file:
        return [parse_sensor(line) for line in file]

def parse_sensor(line: str) -> Sensor:
    matches = re.findall(r'-?\d+', line)
    sensor_pos = Point(int(matches[0]), int(matches[1]))
    beacon_pos = Point(int(matches[2]), int(matches[3]))
    return Sensor(sensor_pos, beacon_pos)




if __name__ == '__main__':
    main()
