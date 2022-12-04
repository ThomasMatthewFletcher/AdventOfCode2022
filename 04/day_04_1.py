from dataclasses import dataclass
from typing import Self

@dataclass
class Range:
    min: int
    max: int

    def contains(self, other: Self):
        return self.min <= other.min and self.max >= other.max

Pair = tuple[Range, Range]

def main():
    pairs = read_pairs()

    count = 0

    for pair in pairs:
        if pair[0].contains(pair[1]) or pair[1].contains(pair[0]):
            count += 1

    print('Count:', count)


def read_pairs():
    with open('04/input.txt', encoding='ascii') as file:
        return [parse_pair(line.strip()) for line in file]

def parse_pair(line: str) -> Pair:
    parts = line.split(',')
    return (parse_range(parts[0]), parse_range(parts[1]))

def parse_range(range_str: str):
    parts = range_str.split('-')
    return Range(int(parts[0]), int(parts[1]))

if __name__ == '__main__':
    main()
