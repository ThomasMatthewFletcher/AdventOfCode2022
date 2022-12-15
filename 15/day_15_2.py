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

    def get_outside_points(self) -> set[Point]:
        points: set[Point] = set()

        for y in range(self.range+2):
            points.add(Point(self.pos.x + y, self.pos.y + (self.range + 1 - y)))
            points.add(Point(self.pos.x + y, self.pos.y - (self.range + 1 - y)))
            points.add(Point(self.pos.x - y, self.pos.y + (self.range + 1 - y)))
            points.add(Point(self.pos.x - y, self.pos.y - (self.range + 1 - y)))

        return points

    def is_inside_range(self, point: Point) -> bool:
        dist = Point.manhatten_dist(self.pos, point)
        return dist <= self.range


def main():
    max_pos = 4000000
    sensors = read_sensors()

    for sensor_index, sensor in enumerate(sensors):
        print('Checking sensor:', sensor_index)
        outside_points = sensor.get_outside_points()
        outside_points = {p for p in outside_points if p.x >= 0 and p.x <= max_pos and p.y >= 0 and p.y <= max_pos}

        for point in outside_points:
            if not is_inside_any_range(point, sensors):
                print('Found:', point)
                print('Tuning Frequency:', point.x * 4000000 + point.y)
                return


def is_inside_any_range(point: Point, sensors: list[Sensor]) -> bool:
    for sensor in sensors:
        if sensor.is_inside_range(point):
            return True
    return False


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
