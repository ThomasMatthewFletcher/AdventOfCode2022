from typing import Union, Literal, Self
import re
from dataclasses import dataclass
from enum import StrEnum, IntEnum

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Point(self.x + other.x, self.y + other.y)

class CubeFace(StrEnum):
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    BACK = 'BACK'
    FRONT = 'FRONT'

class Direction(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

DIRECTION_DELTAS = {
    Direction.RIGHT: Point(1, 0),
    Direction.DOWN: Point(0, 1),
    Direction.LEFT: Point(-1, 0),
    Direction.UP: Point(0, -1)
}

Instruction = Union[int, Literal['L', 'R']]
Tile = Literal[' ', '.', '#']


EDGES: dict[tuple[CubeFace, Direction], tuple[CubeFace, Direction]] = {
    (CubeFace.UP, Direction.RIGHT): (CubeFace.RIGHT, Direction.RIGHT),
    (CubeFace.UP, Direction.DOWN): (CubeFace.FRONT, Direction.DOWN),
    (CubeFace.UP, Direction.LEFT): (CubeFace.LEFT, Direction.RIGHT),
    (CubeFace.UP, Direction.UP): (CubeFace.BACK, Direction.RIGHT),
    (CubeFace.DOWN, Direction.RIGHT): (CubeFace.RIGHT, Direction.LEFT),
    (CubeFace.DOWN, Direction.DOWN): (CubeFace.BACK, Direction.LEFT),
    (CubeFace.DOWN, Direction.LEFT): (CubeFace.LEFT, Direction.LEFT),
    (CubeFace.DOWN, Direction.UP): (CubeFace.FRONT, Direction.UP),
    (CubeFace.LEFT, Direction.RIGHT): (CubeFace.DOWN, Direction.RIGHT),
    (CubeFace.LEFT, Direction.DOWN): (CubeFace.BACK, Direction.DOWN),
    (CubeFace.LEFT, Direction.LEFT): (CubeFace.UP, Direction.RIGHT),
    (CubeFace.LEFT, Direction.UP): (CubeFace.FRONT, Direction.RIGHT),
    (CubeFace.RIGHT, Direction.RIGHT): (CubeFace.DOWN, Direction.LEFT),
    (CubeFace.RIGHT, Direction.DOWN): (CubeFace.FRONT, Direction.LEFT),
    (CubeFace.RIGHT, Direction.LEFT): (CubeFace.UP, Direction.LEFT),
    (CubeFace.RIGHT, Direction.UP): (CubeFace.BACK, Direction.UP),
    (CubeFace.BACK, Direction.RIGHT): (CubeFace.DOWN, Direction.UP),
    (CubeFace.BACK, Direction.DOWN): (CubeFace.RIGHT, Direction.DOWN),
    (CubeFace.BACK, Direction.LEFT): (CubeFace.UP, Direction.DOWN),
    (CubeFace.BACK, Direction.UP): (CubeFace.LEFT, Direction.UP),
    (CubeFace.FRONT, Direction.RIGHT): (CubeFace.RIGHT, Direction.UP),
    (CubeFace.FRONT, Direction.DOWN): (CubeFace.DOWN, Direction.DOWN),
    (CubeFace.FRONT, Direction.LEFT): (CubeFace.LEFT, Direction.DOWN),
    (CubeFace.FRONT, Direction.UP): (CubeFace.UP, Direction.UP)
}

FACE_SIZE = 50

FACE_POSITIONS = {
    CubeFace.UP: Point(1, 0),
    CubeFace.RIGHT: Point(2, 0),
    CubeFace.FRONT: Point(1, 1),
    CubeFace.LEFT: Point(0, 2),
    CubeFace.DOWN: Point(1, 2),
    CubeFace.BACK: Point(0, 3)
}

class Board:
    board_map: list[list[Tile]]

    def __init__(self, board_map: list[list[Tile]]):
        self.board_map = board_map

    def start_position(self) -> Point:
        y = 0
        x = self.board_map[y].index('.')
        return Point(x, y)

    def get_tile_at(self, point: Point) -> Tile:
        if point.y < 0 or point.y >= len(self.board_map):
            return ' '

        if point.x < 0 or point.x >= len(self.board_map[point.y]):
            return ' '

        return self.board_map[point.y][point.x]

    def get_cube_face_at(self, point: Point) -> CubeFace:
        for face, face_position in FACE_POSITIONS.items():
            real_x = face_position.x * FACE_SIZE
            real_y = face_position.y * FACE_SIZE

            if point.x < real_x or point.x >= real_x + FACE_SIZE:
                continue

            if point.y < real_y or point.y >= real_y + FACE_SIZE:
                continue

            return face

        raise Exception('Point is not on a cube face')

    def next_tile_position(self, position: Point, direction: Direction) -> tuple[Point, Direction]:
        delta = DIRECTION_DELTAS[direction]
        next_tile_pos = position + delta
        next_tile = self.get_tile_at(next_tile_pos)
        next_direction = direction

        if next_tile == ' ':
            current_cube_face = self.get_cube_face_at(position)
            current_face_position_x = position.x % FACE_SIZE
            current_face_position_y = position.y % FACE_SIZE

            cube_face_offset_x = position.x - current_face_position_x
            cube_face_offset_y = position.y - current_face_position_y

            if direction == Direction.RIGHT:
                offset = cube_face_offset_y
            elif direction == Direction.DOWN:
                offset = FACE_SIZE - 1 - cube_face_offset_x
            elif direction == Direction.LEFT:
                offset = FACE_SIZE - 1 - cube_face_offset_y
            elif direction == Direction.UP:
                offset = cube_face_offset_x

            next_cube_face, next_direction = EDGES[current_cube_face, direction]
            next_cube_face_position = FACE_POSITIONS[next_cube_face]
            real_x = next_cube_face_position.x * FACE_SIZE
            real_y = next_cube_face_position.y * FACE_SIZE

            if next_direction == Direction.RIGHT:
                next_tile_pos = Point(real_x, real_y + FACE_SIZE - 1 - offset)
            if next_direction == Direction.DOWN:
                next_tile_pos = Point(real_x + offset, real_y)
            elif next_direction == Direction.LEFT:
                next_tile_pos = Point(real_x + FACE_SIZE - 1, real_y + offset)
            elif next_direction == Direction.UP:
                next_tile_pos = Point(real_x + offset, real_y + FACE_SIZE - 1)

        return next_tile_pos, next_direction


class Player:
    position: Point
    direction_index: int
    board: Board

    def __init__(self, board: Board):
        self.board = board
        self.position = board.start_position()
        self.direction_index = 0

    def direction(self) -> Direction:
        return Direction(self.direction_index)

    def turn(self, direction: Literal['L', 'R']):
        direction_value = 1 if direction == 'R' else -1
        self.direction_index = (self.direction_index + direction_value) % 4

    def move(self, spaces: int):
        for _ in range(spaces):
            if not self.move_one_space():
                return

    def move_one_space(self):
        next_tile_position, next_direction = self.board.next_tile_position(self.position, self.direction())
        if self.board.get_tile_at(next_tile_position) != '.':
            return False

        self.position = next_tile_position
        self.direction_index = next_direction.value
        return True


def main():
    board, instructions = parse_input()
    player = Player(board)

    for instruction in instructions:
        if isinstance(instruction, int):
            player.move(instruction)
        else:
            player.turn(instruction)

    password = (player.position.y + 1) * 1000 + (player.position.x + 1) * 4 + player.direction_index
    print('Password:', password)


def parse_input() -> tuple[Board, list[Instruction]]:
    with open('22/input.txt', encoding='ascii') as file:
        lines = [line.rstrip() for line in file]

    board_map = [parse_board_line(line) for line in lines[:-2]]
    board = Board(board_map)

    instructions_line = lines[-1]
    instruction_parts: list[str] = re.findall(r'(L|R|\d+)', instructions_line)
    instructions = list(map(parse_instruction, instruction_parts))

    return board, instructions


def parse_board_line(line: str) -> list[Tile]:
    tiles: list[Tile] = []

    for tile in line:
        assert tile in ('.', '#', ' ')
        tiles.append(tile)
    return tiles

def parse_instruction(instruction: str) -> Instruction:
    if instruction.isdigit():
        return int(instruction)
    if instruction == 'L' or instruction == 'R':
        return instruction
    raise Exception('Invalid instruction')


if __name__ == '__main__':
    main()
