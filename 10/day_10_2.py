from typing import NamedTuple

class Instruction(NamedTuple):
    type: str
    value: int | None

class Crt:
    WIDTH = 40
    HEIGHT = 6
    PIXELS = WIDTH * HEIGHT

    data: list[bool]
    current_pixel: int

    def __init__(self):
        self.data = [False] * Crt.PIXELS
        self.current_pixel = 0

    def set_pixel(self, cycle: int, register_x: int):
        self.current_pixel = cycle - 1
        x_pos = self.current_pixel % 40
        self.data[self.current_pixel] = abs(x_pos - register_x) <= 1

    def __str__(self):
        output = ''

        for row in range(Crt.HEIGHT):
            for col in range(Crt.WIDTH):
                pixel_index = row * Crt.WIDTH + col
                output += '#' if self.data[pixel_index] else '.'

            output += '\n'

        return output


def main():
    instructions = read_instructions()

    crt = Crt()

    register_x = 1
    cycle = 1

    instruction_pointer = 0
    instruction_step = 0

    while cycle < Crt.PIXELS:
        crt.set_pixel(cycle, register_x)

        instruction = instructions[instruction_pointer]

        if instruction.type == 'noop':
            instruction_pointer += 1
        else:
            if instruction_step == 0:
                instruction_step += 1
            else:
                instruction_pointer += 1
                instruction_step = 0
                register_x += instruction.value

        cycle += 1

    print(crt)


def read_instructions():
    with open('10/input.txt', encoding='ascii') as file:
        return [parse_instruction(line) for line in file]

def parse_instruction(line: str):
    parts = line.split()
    value = None

    if len(parts) == 2:
        value = int(parts[1])

    return Instruction(parts[0], value)

if __name__ == '__main__':
    main()
