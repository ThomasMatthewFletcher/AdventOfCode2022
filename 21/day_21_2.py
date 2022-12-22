from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Monkey(ABC):
    name: str

    @abstractmethod
    def get_value(self) -> int:
        pass

    @abstractmethod
    def contains_human(self) -> bool:
        pass


@dataclass
class IntMonkey(Monkey):
    value: int

    def get_value(self) -> int:
        return self.value

    def contains_human(self) -> bool:
        return self.name == 'humn'

@dataclass
class ExpressionMonkey(Monkey):
    left_name: str
    operation: str
    right_name: str
    left: Monkey | None = None
    right: Monkey | None = None

    def set_monkeys(self, monkeys: dict[str, Monkey]):
        self.left = monkeys[self.left_name]
        self.right = monkeys[self.right_name]

    def get_value(self) -> int:
        assert self.left and self.right
        left = self.left.get_value()
        right = self.right.get_value()

        match self.operation:
            case '+': return left + right
            case '-': return left - right
            case '*': return left * right
            case '/': return left // right
            case _: raise Exception('Invalid operation')

    def contains_human(self) -> bool:
        assert self.left and self.right
        return self.left.contains_human() or self.right.contains_human()


def main():
    monkeys = read_monkeys()

    for monkey in monkeys.values():
        if isinstance(monkey, ExpressionMonkey):
            monkey.set_monkeys(monkeys)

    root = monkeys['root']
    assert isinstance(root, ExpressionMonkey) and root.left and root.right

    monkey_containing_human = None
    monkey_not_containing_human = None

    if root.left.contains_human():
        monkey_containing_human = root.left
        monkey_not_containing_human = root.right
    else:
        monkey_containing_human = root.right
        monkey_not_containing_human = root.left

    target = monkey_not_containing_human.get_value()

    while isinstance(monkey_containing_human, ExpressionMonkey):
        assert monkey_containing_human.left and monkey_containing_human.right

        left_contains_human = monkey_containing_human.left.contains_human()

        if left_contains_human:
            next_monkey_containing_human = monkey_containing_human.left
            next_monkey_not_containing_human = monkey_containing_human.right
        else:
            next_monkey_containing_human = monkey_containing_human.right
            next_monkey_not_containing_human = monkey_containing_human.left

        not_containing_human_value = next_monkey_not_containing_human.get_value()

        if monkey_containing_human.operation == '+':
            target = target - not_containing_human_value
        elif monkey_containing_human.operation == '*':
            target = target // not_containing_human_value
        elif monkey_containing_human.operation == '-':
            if left_contains_human:
                target = target + not_containing_human_value
            else:
                target = not_containing_human_value - target
        elif monkey_containing_human.operation == '/':
            if left_contains_human:
                target = target * not_containing_human_value
            else:
                target = not_containing_human_value // target

        monkey_containing_human = next_monkey_containing_human
        monkey_not_containing_human = next_monkey_not_containing_human

    print('Target:', target)



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
