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

    def get_top_state(self) -> str:
        output = ''

        for y in range(self.height - 20, self.height + 1):
            for x in range(self.width):
                if Point(x, y) in self.rocks:
                    output += '#'
                else:
                    output += '.'

        return output


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

    steps = len(jets) * 5
    total_steps = 0

    states: dict[str, tuple[int, int]] = {}

    extra_height = 0
    remaining_steps = 0

    while True:
        print('Steps so far:', total_steps)

        for _ in range(steps):
            chamber.add_rock()

        total_steps += steps
        state = chamber.tower.get_top_state()

        if state in states:
            print('Already seen this state')
            print('Steps so far:', total_steps)
            height_since_last_seen = chamber.tower.height - states[state][0]
            print('Height since last seen:', height_since_last_seen)
            steps_since_last_seen = total_steps - states[state][1]
            print('Steps since last seen:', steps_since_last_seen)

            remaining_chunks = (1000000000000 - total_steps) // steps_since_last_seen
            total_steps += remaining_chunks * steps_since_last_seen
            remaining_steps = 1000000000000 - total_steps
            extra_height = remaining_chunks * height_since_last_seen

            print('New total steps:', total_steps)
            print('New height:', chamber.tower.height)

            break

        else:
            states[state] = (chamber.tower.height, total_steps)

    for _ in range(remaining_steps):
        chamber.add_rock()

    print('Total height:', chamber.tower.height + extra_height)


def read_jets():
    with open('17/input.txt', encoding='ascii') as file:
        return list(file.readline().strip())


if __name__ == '__main__':
    main()
