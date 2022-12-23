from dataclasses import dataclass
from collections import defaultdict
from typing import Self

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Self):
        return Point(self.x + other.x, self.y + other.y)

DIRECTION_CHECKS = [
    (Point(0, -1), [Point(-1, -1), Point(0, -1), Point(1, -1)]),
    (Point(0, 1),  [Point(-1, 1), Point(0, 1), Point(1, 1)]),
    (Point(-1, 0), [Point(-1, -1), Point(-1, 0), Point(-1, 1)]),
    (Point(1, 0),  [Point(1, -1), Point(1, 0), Point(1, 1)]),
]

def main():
    elf_positions = read_elf_positions()

    for round in range(10):
        elf_positions = do_round(elf_positions, round)

    empty_spaces = count_empty_spaces(elf_positions)
    print('Empty spaces:', empty_spaces)


def print_elves(elf_positions: set[Point]):
    min_x = min(p.x for p in elf_positions)
    max_x = max(p.x for p in elf_positions)
    min_y = min(p.y for p in elf_positions)
    max_y = max(p.y for p in elf_positions)

    output = ''

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if Point(x, y) in elf_positions:
                output += '#'
            else:
                output += '.'
        output += '\n'

    print(output)


def do_round(current_positions: set[Point], round: int) -> set[Point]:
    proposed_moves: dict[Point, Point] = {}
    proposed_count: defaultdict[Point, int] = defaultdict(int)

    # Propose new positions
    for current_position in current_positions:
        proposed_position = propose_position(current_position, current_positions, round)
        proposed_moves[current_position] = proposed_position
        proposed_count[proposed_position] += 1

    # Move
    new_positions: set[Point] = set()

    for from_position, to_position in proposed_moves.items():
        if proposed_count[to_position] == 1:
            new_positions.add(to_position)
        else:
            new_positions.add(from_position)

    return new_positions


def propose_position(current_position: Point, elf_positions: set[Point], round: int) -> Point:
    if not has_elf_neighbour(current_position, elf_positions):
        return current_position

    for check_offset in range(4):
        move, checks = DIRECTION_CHECKS[(round + check_offset) % 4]
        move_position = current_position + move

        if check_positions(current_position, elf_positions, checks):
            return move_position
    return current_position


def has_elf_neighbour(current_position: Point, elf_positions: set[Point]) -> bool:
    for y in range(-1, 2):
        for x in range(-1, 2):
            if y == 0 and x == 0:
                continue

            check_position = Point(current_position.x + x, current_position.y + y)

            if check_position in elf_positions:
                return True

    return False


def check_positions(current_position: Point, elf_positions: set[Point], checks: list[Point]) -> bool:
    for check in checks:
        check_position = current_position + check

        if check_position in elf_positions:
            return False

    return True


def count_empty_spaces(elf_positions: set[Point]):
    min_x = min(p.x for p in elf_positions)
    max_x = max(p.x for p in elf_positions)
    min_y = min(p.y for p in elf_positions)
    max_y = max(p.y for p in elf_positions)

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    print('Width:', width)
    print('Height:', height)

    total_spaces = width * height
    occupied_spaces = len(elf_positions)
    return total_spaces - occupied_spaces


def read_elf_positions() -> set[Point]:
    elf_positions: set[Point] = set()

    with open('23/input.txt', encoding='ascii') as file:
        for y, line in enumerate(file):
            for x, char in enumerate(line):
                if char == '#':
                    elf_positions.add(Point(x, y))

    return elf_positions

if __name__ == '__main__':
    main()
