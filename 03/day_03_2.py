from functools import reduce

def main():
    rucksacks = read_rucksack_items()

    total = 0

    for group in chunk(rucksacks):
        item = find_shared_item(group)
        total += get_priority(item)

    print('Sum of priorities:', total)

def chunk(lst):
    for i in range(0, len(lst), 3):
        yield lst[i:i + 3]

def find_shared_item(group: list[set[str]]):
    return reduce(lambda acc, rucksack: acc.intersection(rucksack), group).pop()

def read_rucksack_items():
    with open('03/input.txt', encoding='ascii') as file:
        return [set(line.strip()) for line in file]

def get_priority(item: str):
    if item >= 'a' and item <= 'z':
        return ord(item) - ord('a') + 1
    if item >= 'A' and item <= 'Z':
        return ord(item) - ord('A') + 27
    raise Exception(f'Invalid item: {item}')

if __name__ == '__main__':
    main()
