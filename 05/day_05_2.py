from dataclasses import dataclass
import re
import os
import math
import time

def clear():
    os.system('clear')

@dataclass
class Step:
    count: int
    from_stack: int
    to_stack: int

class CrateMap:
    stacks: list[list[str]]
    stack_count: int
    max_height: int

    def __init__(self, stacks: list[list[str]]):
        self.stacks = stacks
        self.stack_count = len(stacks)
        self.max_height = 50

    def move(self, from_stack: int, to_stack: int, count: int):
        crates = self.stacks[from_stack-1][-count:]
        del self.stacks[from_stack-1][-count:]

        self.stacks[to_stack-1].extend(crates)

    def __str__(self):
        map_str = ''

        for height in range(self.max_height-1, -1, -1):
            for stack in self.stacks:
                if height < len(stack):
                    map_str += f'[{stack[height]}] '
                else:
                    map_str += '    '
            map_str += '\n'

        for stack_index, stack in enumerate(self.stacks):
            map_str += f' {stack_index + 1}  '

        return map_str

    def top_crates(self):
        return [stack[-1] for stack in self.stacks]


class Progress:
    total: int
    current: int
    WIDTH = 20

    def __init__(self, total: int):
        self.total = total
        self.current = 0

    def percent(self):
        return (self.current / self.total) * 100

    def bar_str(self):
        complete_bars = math.floor(Progress.WIDTH * self.current / self.total)
        incomplete_bars = Progress.WIDTH - complete_bars
        return '[' + '=' * complete_bars + '.' * incomplete_bars + ']'

    def __str__(self):
        return f'{self.bar_str()} {self.current} / {self.total} ({self.percent():.2f}%)'


def main():
    crate_map, procedure = parse_instructions()

    progress = Progress(len(procedure))

    clear()
    print(crate_map)
    print()
    print(progress)
    time.sleep(5)

    for step in procedure:
        progress.current += 1

        crate_map.move(step.from_stack, step.to_stack, step.count)
        clear()
        print(crate_map)
        print()
        print(progress)

    print()
    print('Top crates:', ''.join(crate_map.top_crates()))


def parse_instructions():
    with open('05/input.txt', encoding='ascii') as file:
        crate_map_part, procedure_part = file.read().split('\n\n')

    crate_map = parse_crate_map(crate_map_part)
    procedure = parse_procedure(procedure_part)

    return crate_map, procedure


def parse_crate_map(crate_map_str: str):
    lines = crate_map_str.split('\n')
    stack_numbers = lines.pop().split()
    last_stack = int(stack_numbers[-1])

    stacks = [[] for _ in range(last_stack)]

    for line in lines:
        for stack in range(last_stack):
            char_index = stack * 4 + 1

            if char_index < len(line):
                char = line[char_index]
                if char != ' ':
                    stacks[stack].insert(0, char)

    return CrateMap(stacks)

def parse_procedure(procedure_str: str):
    steps: list[Step] = []

    for line in procedure_str.split('\n'):
        result = re.match(r'move (\d+) from (\d+) to (\d+)', line)
        values = map(int, result.groups())
        steps.append(Step(*values))

    return steps


if __name__ == '__main__':
    main()
