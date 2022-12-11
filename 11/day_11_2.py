
from typing import Callable
from dataclasses import dataclass

@dataclass
class Monkey:
    items: list[int]
    operation: Callable[[int], int]
    test_divisible: int
    if_true: int
    if_false: int
    inspected_items = 0

MONKEYS = [
    Monkey(
        items=[72, 64, 51, 57, 93, 97, 68],
        operation=lambda old: old * 19,
        test_divisible=17,
        if_true=4,
        if_false=7
    ),
    Monkey(
        items=[62],
        operation=lambda old: old * 11,
        test_divisible=3,
        if_true=3,
        if_false=2
    ),
    Monkey(
        items=[57, 94, 69, 79, 72],
        operation=lambda old: old + 6,
        test_divisible=19,
        if_true=0,
        if_false=4
    ),
    Monkey(
        items=[80, 64, 92, 93, 64, 56],
        operation=lambda old: old + 5,
        test_divisible=7,
        if_true=2,
        if_false=0
    ),
    Monkey(
        items=[70, 88, 95, 99, 78, 72, 65, 94],
        operation=lambda old: old + 7,
        test_divisible=2,
        if_true=7,
        if_false=5
    ),
    Monkey(
        items=[57, 95, 81, 61],
        operation=lambda old: old * old,
        test_divisible=5,
        if_true=1,
        if_false=6
    ),
    Monkey(
        items=[79, 99],
        operation=lambda old: old + 2,
        test_divisible=11,
        if_true=3,
        if_false=1
    ),
    Monkey(
        items=[68, 98, 62],
        operation=lambda old: old + 3,
        test_divisible=13,
        if_true=5,
        if_false=6
    )
]

# MONKEYS = [
#     Monkey(
#         items=[79, 98],
#         operation=lambda old: old * 19,
#         test_divisible=23,
#         if_true=2,
#         if_false=3
#     ),
#     Monkey(
#         items=[54, 65, 75, 74],
#         operation=lambda old: old + 6,
#         test_divisible=19,
#         if_true=2,
#         if_false=0
#     ),
#     Monkey(
#         items=[79, 60, 97],
#         operation=lambda old: old * old,
#         test_divisible=13,
#         if_true=1,
#         if_false=3
#     ),
#     Monkey(
#         items=[74],
#         operation=lambda old: old + 3,
#         test_divisible=17,
#         if_true=0,
#         if_false=1
#     )
# ]


def main():
    mult_divisible = 1

    for monkey in MONKEYS:
        mult_divisible *= monkey.test_divisible

    for _ in range(10000):
        for monkey in MONKEYS:
            while monkey.items:
                monkey.inspected_items += 1
                item = monkey.items.pop(0)
                item = monkey.operation(item)
                item = item % mult_divisible

                is_divisible = item % monkey.test_divisible == 0
                new_monkey = monkey.if_true if is_divisible else monkey.if_false
                MONKEYS[new_monkey].items.append(item)


    sorted_monkeys = sorted([m.inspected_items for m in MONKEYS])

    monkey_business = sorted_monkeys[-1] * sorted_monkeys[-2]
    print('Monkey business:', monkey_business)


if __name__ == '__main__':
    main()
