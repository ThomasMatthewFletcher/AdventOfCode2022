
Cube = tuple[int, int, int]

DIRECTIONS: list[Cube] = [
    (0, 0, 1),
    (0, 0, -1),
    (0, 1, 0),
    (0, -1, 0),
    (1, 0, 0),
    (-1, 0, 0)
]

def main():
    cubes = read_cubes()

    mins: Cube = tuple([min(cube[d] for cube in cubes) - 1 for d in range(3)])
    maxs: Cube = tuple([max(cube[d] for cube in cubes) + 1 for d in range(3)])

    steam_cubes: set[Cube] = {mins}
    queue: list[Cube] = [maxs]

    while queue:
        cube = queue.pop(0)

        for direction in DIRECTIONS:
            other_cube = tuple(sum(v) for v in zip(cube, direction))

            if other_cube in steam_cubes:
                continue

            if other_cube in cubes:
                continue

            if not is_cube_in_big_cube(other_cube, mins, maxs):
                continue

            steam_cubes.add(other_cube)
            queue.append(other_cube)

    steam_surface_area = surface_area_of_cubes(steam_cubes)
    outside_surface_area = surface_area_of_cube(
        maxs[0] - mins[0] + 1,
        maxs[1] - mins[1] + 1,
        maxs[2] - mins[2] + 1
    )

    print('Steam surface area:', steam_surface_area)
    print('Steam outside surface area:', outside_surface_area)

    lava_surface_area = steam_surface_area - outside_surface_area

    print('Lava surface area:', lava_surface_area)



def is_cube_in_big_cube(cube: Cube, mins: Cube, maxs: Cube):
    for dim in range(3):
        if cube[dim] < mins[dim] or cube[dim] > maxs[dim]:
            return False

    return True


def surface_area_of_cube(length: int, width: int, height: int) -> int:
    return (length * width * 2) + (length * height * 2) + (width * height * 2)


def surface_area_of_cubes(cubes: set[Cube]) -> int:
    surface_area = 0

    for cube in cubes:
        for direction in DIRECTIONS:
            other_cube = tuple(sum(v) for v in zip(cube, direction))

            if other_cube not in cubes:
                surface_area += 1

    return surface_area



def read_cubes() -> set[Cube]:
    with open('18/input.txt', encoding='ascii') as file:
        return {tuple(map(int, line.strip().split(','))) for line in file}


if __name__ == '__main__':
    main()
