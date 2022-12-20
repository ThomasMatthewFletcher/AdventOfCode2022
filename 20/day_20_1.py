
def main():
    numbers = read_numbers()

    indices = list(range(len(numbers)))

    for i, value in enumerate(numbers):
        current_index = indices.index(i)
        new_index = (current_index + value) % (len(numbers) - 1)

        indices.pop(current_index)
        indices.insert(new_index, i)

    new_numbers = [numbers[i] for i in indices]
    zero_index = new_numbers.index(0)

    grove_coordinates = 0

    for i in [1000, 2000, 3000]:
        grove_coordinates += new_numbers[(zero_index + i) % len(numbers)]

    print('Grove coordinates:', grove_coordinates)

def read_numbers():
    with open('20/input.txt', encoding='ascii') as file:
        return [int(line) for line in file]


if __name__ == '__main__':
    main()
