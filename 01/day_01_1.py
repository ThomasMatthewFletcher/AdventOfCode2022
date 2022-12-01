
def main():
    elves_calories = read_elves_calories()

    total_calories = [sum(elf_calories) for elf_calories in elves_calories]
    max_calories = max(total_calories)

    print('Max calories:', max_calories)


def read_elves_calories():
    with open('01/input.txt', encoding='utf-8') as file:
        data = file.read()

    return [[int(l) for l in elf.split('\n')] for elf in data.split('\n\n')]


if __name__ == '__main__':
    main()
