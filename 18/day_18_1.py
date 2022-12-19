
DIRECTIONS = [
    (0, 0, 1),
    (0, 0, -1),
    (0, 1, 0),
    (0, -1, 0),
    (1, 0, 0),
    (-1, 0, 0)
]

def main():
    cubes = read_cubes()

    surface_area = 0

    for cube in cubes:
        for direction in DIRECTIONS:
            other_cube = tuple(sum(v) for v in zip(cube, direction))

            if other_cube not in cubes:
                surface_area += 1

    print('Total surface area:', surface_area)



def read_cubes() -> set[tuple[int, int, int]]:
    with open('18/input.txt', encoding='ascii') as file:
        return {tuple(map(int, line.strip().split(','))) for line in file}


if __name__ == '__main__':
    main()
