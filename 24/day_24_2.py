from dataclasses import dataclass
from typing import Self
from enum import StrEnum

class Direction(StrEnum):
    NORTH = '^'
    EAST = '>'
    SOUTH = 'v'
    WEST = '<'

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Point(self.x + other.x, self.y + other.y)

DIRECTIONS = {
    Direction.NORTH: Point(0, -1),
    Direction.EAST:  Point(1, 0),
    Direction.SOUTH: Point(0, 1),
    Direction.WEST:  Point(-1, 0)
}


@dataclass
class Blizzard:
    position: Point
    direction: Direction

    def move(self, width: int, height: int):
        self.position = Point(
            (self.position.x + DIRECTIONS[self.direction].x) % width,
            (self.position.y + DIRECTIONS[self.direction].y) % height
        )

class Valley:
    width: int
    height: int
    entrance_position: Point
    exit_position: Point
    blizzards: list[Blizzard]

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.entrance_position = Point(0, -1)
        self.exit_position = Point(width - 1, height)
        self.blizzards = []

    def add_blizzard(self, position: Point, direction: Direction):
        self.blizzards.append(Blizzard(position, direction))

    def move_blizzards(self):
        for blizzard in self.blizzards:
            blizzard.move(self.width, self.height)

    def get_blizard_positions(self) -> set[Point]:
        return {b.position for b in self.blizzards}

    def __str__(self):
        output = ''

        for y in range(-1, self.height + 1):
            for x in range(-1, self.width + 1):
                pos = Point(x, y)

                if x == -1 or x == self.width:
                    output += '#'
                elif y == -1 or y == self.height:
                    if pos == self.entrance_position or pos == self.exit_position:
                        output += '.'
                    else:
                        output += '#'
                else:
                    blizzards = [b for b in self.blizzards if b.position == pos]

                    if len(blizzards) == 0:
                        output += '.'
                    elif len(blizzards) == 1:
                        output += str(blizzards[0].direction)
                    elif len(blizzards) <= 9:
                        output += str(len(blizzards))
                    else:
                        output += '+'

            output += '\n'

        return output

@dataclass(frozen=True)
class State:
    time: int
    position: Point

def main():
    valley = read_valley()

    blizzard_positions_at_time: dict[int, set[Point]] = {}

    start_time = 0
    start_position = valley.entrance_position

    for end_position in [valley.exit_position, valley.entrance_position, valley.exit_position]:
        print()
        print('Start time:', start_time)
        print('Start position:', start_position)
        print('End position:', end_position)

        initial_state = State(start_time, start_position)

        queue = [initial_state]
        dist = {initial_state: start_time}

        while queue:
            state = queue.pop(0)
            # print('State:', state)

            if state.position == end_position:
                start_position = end_position
                start_time = dist[state]
                print('Total time:', dist[state])
                break

            if (state.time + 1) not in blizzard_positions_at_time:
                valley.move_blizzards()
                blizzard_positions_at_time[state.time + 1] = valley.get_blizard_positions()
                # print(valley)

            blizzard_positions = blizzard_positions_at_time[state.time + 1]

            neighbours = get_neighbours(state, blizzard_positions, valley)
            # print(neighbours)

            for neighbour in neighbours:
                if neighbour not in dist:
                    queue.append(neighbour)
                    dist[neighbour] = dist[state] + 1


def get_neighbours(state: State, blizzard_positions: set[Point], valley: Valley):
    neighbours: list[State] = []

    for direction in DIRECTIONS.values():
        new_position = state.position + direction

        if new_position.x < 0 or new_position.x >= valley.width:
            continue

        if (new_position.y < 0 or new_position.y >= valley.height) and (new_position != valley.exit_position) and (new_position != valley.entrance_position):
            continue

        if new_position in blizzard_positions:
            continue

        neighbours.append(State(state.time + 1, new_position))

    if state.position not in blizzard_positions:
        neighbours.append(State(state.time + 1, state.position))

    return neighbours



def read_valley():
    with open('24/input.txt', encoding='ascii') as file:
        lines = [line.strip() for line in file]

    width = len(lines[0]) - 2
    height = len(lines) - 2

    valley = Valley(width, height)

    for y, line in enumerate(lines[1:-1]):
        for x, cell in enumerate(line[1:-1]):
            if cell in ('^', '>', 'v', '<'):
                direction = Direction(cell)
                position = Point(x, y)
                valley.add_blizzard(position, direction)

    return valley


if __name__ == '__main__':
    main()
