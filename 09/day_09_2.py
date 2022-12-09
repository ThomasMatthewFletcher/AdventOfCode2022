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
    points: list[Point]
    tail_visited: set[Point]

    def __init__(self, length: int):
        self.points = [Point(0, 0) for _ in range(length)]
        self.tail_visited = {self.points[-1]}

    def move_head(self, motion: Motion):
        for _ in range(motion.count):
            self.points[0] += motion.dir
            for i in range(len(self.points)-1):
                self._move_tail(i)
            self.tail_visited.add(self.points[-1])

    def _move_tail(self, head_index: int):
        head = self.points[head_index]
        tail = self.points[head_index+1]
        delta = head - tail

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

            self.points[head_index+1] += Point(dx, dy)

def main():
    motions = read_motions()
    rope = Rope(10)

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
