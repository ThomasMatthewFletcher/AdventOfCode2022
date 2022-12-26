
SNAFU_CHARACTERS = {'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}
SNAFU_DIGITS = {x: y for (y, x) in SNAFU_CHARACTERS.items()}

def main():
    snafu_fuel_requirements = read_fuel_requirements()
    decimal_fuel_requirements = list(map(snafu_to_decimal, snafu_fuel_requirements))

    total_fuel_requirements = sum(decimal_fuel_requirements)
    snafu_total_fuel_requirements = decimal_to_snafu(total_fuel_requirements)
    print(snafu_total_fuel_requirements)


def snafu_to_decimal(snafu: str) -> int:
    total = 0

    for position, snafu_char in enumerate(reversed(snafu)):
        digit = SNAFU_CHARACTERS[snafu_char]
        total += digit * (5 ** position)

    return total

def decimal_to_snafu(decimal: int) -> str:
    snafu: list[str] = []
    remaining = decimal
    position = 0

    while remaining != 0:
        digit_value = (remaining + 2) % 5 - 2
        remaining -= digit_value
        remaining //= 5
        snafu.insert(0, SNAFU_DIGITS[digit_value])
        position += 1

    return ''.join(snafu)


def read_fuel_requirements() -> list[str]:
    with open('25/input.txt', encoding='ascii') as file:
        return [line.strip() for line in file]

if __name__ == '__main__':
    main()
