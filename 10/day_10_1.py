from typing import NamedTuple


class Instruction(NamedTuple):
    type: str
    value: int | None

def main():
    instructions = read_instructions()
    register_x = 1
    cycle = 1

    instruction_pointer = 0
    instruction_step = 0

    signal_strength_sum = 0

    while cycle < 220:
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

        if (cycle + 20) % 40 == 0:
            signal_strength_sum += cycle * register_x

    print('Signal strength sum:', signal_strength_sum)


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
