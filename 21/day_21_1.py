from dataclasses import dataclass
from abc import ABC

@dataclass
class Monkey(ABC):
    name: str

@dataclass
class IntMonkey(Monkey):
    value: int

@dataclass
class ExpressionMonkey(Monkey):
    left: str
    operation: str
    right: str

def main():
    monkeys = read_monkeys()
    root_result = calculate('root', monkeys)
    print('Root result:', root_result)


def calculate(name: str, monkeys: dict[str, Monkey]) -> int:
    monkey = monkeys[name]

    if isinstance(monkey, IntMonkey):
        return monkey.value
    elif isinstance(monkey, ExpressionMonkey):
        left = calculate(monkey.left, monkeys)
        right = calculate(monkey.right, monkeys)

        match monkey.operation:
            case '+': return left + right
            case '-': return left - right
            case '*': return left * right
            case '/': return left // right
            case _: raise Exception('Invalid operation')
    else:
        raise Exception('Invalid monkey')


def read_monkeys():
    with open('21/input.txt', encoding='ascii') as file:
        monkeys = [parse_monkey(line) for line in file]
        return {monkey.name: monkey for monkey in monkeys}

def parse_monkey(line: str) -> Monkey:
    # sjmn: drzm * dbpl
    parts = line.split()
    name = parts[0][:-1]

    if len(parts) == 2:
        return IntMonkey(name, int(parts[1]))
    else:
        return ExpressionMonkey(name, parts[1], parts[2], parts[3])

if __name__ == '__main__':
    main()

