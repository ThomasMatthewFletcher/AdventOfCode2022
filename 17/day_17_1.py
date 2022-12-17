from typing import Iterable, NamedTuple
from itertools import cycle

class Point(NamedTuple):
    x: int
    y: int

Rock = set[Point]

ROCK_TYPES: Iterable[Rock] = cycle([
    {Point(0,0),Point(1,0),Point(2,0),Point(3,0)},
    {Point(1,0),Point(0,1),Point(1,1),Point(2,1),Point(1,2)},
    {Point(0,0),Point(1,0),Point(2,0),Point(2,1),Point(2,2)},
    {Point(0,0),Point(0,1),Point(0,2),Point(0,3)},
    {Point(0,0),Point(1,0),Point(0,1),Point(1,1)}
])

JET_DIRECTION = {'>': 1, '<': -1}

class Tower:
    rocks: set[Point]
    width: int
    height: int

    def __init__(self, width: int):
        self.rocks = set()
        self.width = width
        self.height = 0

    def add_rock(self, rock: Rock, pos: Point):
        for part in rock:
            part_pos = Point(pos.x + part.x, pos.y + part.y)
            self.rocks.add(part_pos)

            if part_pos.y + 1 > self.height:
                self.height = part_pos.y + 1

    def is_rock_collision(self, rock: Rock, pos: Point) -> bool:
        for part in rock:
            part_pos = Point(pos.x + part.x, pos.y + part.y)

            if part_pos.x < 0 or part_pos.x >= self.width or part_pos.y < 0:
                return True

            if part_pos in self.rocks:
                return True

        return False


class Chamber:
    jets: Iterable[str]
    tower: Tower

    def __init__(self, jets: list[str]):
        self.jets = cycle(jets)
        self.next_rock = 0
        self.next_jet = 0
        self.tower = Tower(7)

    def add_rock(self):
        rock: Rock = next(ROCK_TYPES)

        x = 2
        y = self.tower.height + 3

        while True:
            # Jet - horizontal movement

            jet: str = next(self.jets)
            next_x = x + JET_DIRECTION[jet]

            if not self.tower.is_rock_collision(rock, Point(next_x, y)):
                x = next_x

            # Gravity - vertical movement

            if not self.tower.is_rock_collision(rock, Point(x, y - 1)):
                y -= 1
            else:
                self.tower.add_rock(rock, Point(x, y))
                break





def main():
    jets = read_jets()
    chamber = Chamber(jets)

    for _ in range(2022):
        chamber.add_rock()

    print('Tower height:', chamber.tower.height)


def read_jets():
    with open('17/input.txt', encoding='ascii') as file:
        return list(file.readline().strip())


if __name__ == '__main__':
    main()
