

Rucksack = tuple[str, str]

def main():
    rucksacks = read_rucksacks()

    total = 0

    for rucksack in rucksacks:
        item = find_shared_item(rucksack)
        total += get_priority(item)

    print('Sum of priorities:', total)


def find_shared_item(rucksack: Rucksack):
    first = set(rucksack[0])
    second = set(rucksack[1])
    return first.intersection(second).pop()

def read_rucksacks():
    with open('03/input.txt', encoding='ascii') as file:
        return [parse_rucksack(line.strip()) for line in file]

def parse_rucksack(line: str) -> Rucksack:
    count = len(line) // 2
    return (line[:count],line[count:])

def get_priority(item: str):
    if item >= 'a' and item <= 'z':
        return ord(item) - ord('a') + 1
    if item >= 'A' and item <= 'Z':
        return ord(item) - ord('A') + 27
    raise Exception(f'Invalid item: {item}')

if __name__ == '__main__':
    main()
