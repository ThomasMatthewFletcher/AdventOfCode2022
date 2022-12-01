
def main():
    elves_calories = read_elves_calories()

    total_calories = [sum(elf_calories) for elf_calories in elves_calories]
    total_calories.sort(reverse=True)
    top_three_sum = sum(total_calories[:3])

    print('Top three calories:', top_three_sum)


def read_elves_calories():
    with open('01/input.txt', encoding='utf-8') as file:
        data = file.read()

    return [[int(l) for l in elf.split('\n')] for elf in data.split('\n\n')]


if __name__ == '__main__':
    main()
