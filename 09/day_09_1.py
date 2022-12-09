from dataclasses import dataclass
from typing import Self

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Self):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self):
        return Point(self.x - other.x, self.y - other.y)

@dataclass
class Motion:
    dir: Point
    count: int

DIRECTIONS = {
    'U': Point( 0, -1),
    'D': Point( 0,  1),
    'L': Point(-1,  0),
    'R': Point( 1,  0)
}

class Rope:
    head: Point
    tail: Point
    tail_visited: set[Point]

    def __init__(self):
        self.head = Point(0, 0)
        self.tail = Point(0, 0)
        self.tail_visited = {self.tail}

    def move_head(self, motion: Motion):
        for _ in range(motion.count):
            self.head += motion.dir
            self._move_tail()
            self.tail_visited.add(self.tail)

    def _move_tail(self):
        delta = self.head - self.tail

        if abs(delta.x) > 1 or abs(delta.y) > 1:
            dx = 0
            dy = 0

            if delta.x > 0:
                dx = 1
            elif delta.x < 0:
                dx = -1

            if delta.y > 0:
                dy = 1
            elif delta.y < 0:
                dy = -1

            self.tail += Point(dx, dy)

def main():
    motions = read_motions()
    rope = Rope()

    for motion in motions:
        rope.move_head(motion)

    print('Tail visited:', len(rope.tail_visited))

def read_motions():
    with open('09/input.txt', encoding='ascii') as file:
        return [parse_motion(line.strip()) for line in file]

def parse_motion(line: str):
    parts = line.split()
    return Motion(DIRECTIONS[parts[0]], int(parts[1]))

if __name__ == '__main__':
    main()
