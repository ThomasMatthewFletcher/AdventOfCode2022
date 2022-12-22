from typing import Union, Literal, Self
import re
from dataclasses import dataclass

Instruction = Union[int, Literal['L', 'R']]
Tile = Literal[' ', '.', '#']

@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Point(self.x + other.x, self.y + other.y)

DIRECTIONS = [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1)]

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


    def next_tile_position(self, position: Point, direction: Point) -> Point:
        next_tile_pos = position + direction
        next_tile = self.get_tile_at(next_tile_pos)

        if next_tile == ' ':
            opposite_direction = Point(direction.x * -1, direction.y * -1)
            next_tile_pos = position
            test_tile_pos = position + opposite_direction

            while self.get_tile_at(test_tile_pos) != ' ':
                next_tile_pos = test_tile_pos
                test_tile_pos += opposite_direction

        return next_tile_pos


class Player:
    position: Point
    direction_index: int
    board: Board

    def __init__(self, board: Board):
        self.board = board
        self.position = board.start_position()
        self.direction_index = 0

    def direction(self) -> Point:
        return DIRECTIONS[self.direction_index]

    def turn(self, direction: Literal['L', 'R']):
        direction_value = 1 if direction == 'R' else -1
        self.direction_index = (self.direction_index + direction_value) % 4

    def move(self, spaces: int):
        for _ in range(spaces):
            if not self.move_one_space():
                return

    def move_one_space(self):
        next_tile_position = self.board.next_tile_position(self.position, self.direction())
        if self.board.get_tile_at(next_tile_position) != '.':
            return False

        self.position = next_tile_position
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
