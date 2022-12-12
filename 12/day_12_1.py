from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int

DIRECTIONS = [Point(-1, 0), Point(1, 0), Point(0, -1), Point(0, 1)]


class HeightMap:
    height_map: list[list[str]]
    width: int
    height: int
    start: Point
    end: Point

    def __init__(self, height_map: list[list[str]], start: Point, end: Point):
        self.height_map = height_map
        self.width = len(height_map[0])
        self.height = len(height_map)
        self.start = start
        self.end = end

    def get_height_at(self, point: Point):
        return self.height_map[point.y][point.x]

    def is_valid_neighbour(self, point: Point, neighbour: Point):
        if neighbour.x < 0 or neighbour.x >= self.width:
            return False

        if neighbour.y < 0 or neighbour.y >= self.height:
            return False

        current_height = self.get_height_at(point)
        neighbour_height = self.get_height_at(neighbour)

        return ord(neighbour_height) <= ord(current_height) + 1


    def get_valid_neighbours(self, point: Point):
        valid_neighbours: list[Point] = []

        for direction in DIRECTIONS:
            neighbour = Point(point.x + direction.x, point.y + direction.y)
            if self.is_valid_neighbour(point, neighbour):
                valid_neighbours.append(neighbour)

        return valid_neighbours




    @classmethod
    def from_input_lines(cls, lines: list[str]):
        rows: list[list[str]] = []
        start: Point | None = None
        end: Point | None = None

        for y, line in enumerate(lines):
            row: list[int] = []

            for x, cell in enumerate(line.strip()):
                if cell == 'S':
                    start = Point(x, y)
                    cell = 'a'
                elif cell == 'E':
                    end = Point(x, y)
                    cell = 'z'

                row.append(cell)
            rows.append(row)

        assert start and end
        return HeightMap(rows, start, end)



def main():
    height_map = read_height_map()

    queue = [height_map.start]
    distances: dict[Point, int] = {height_map.start: 0}

    while queue:
        current = queue.pop(0)

        if current == height_map.end:
            break

        neighbours = height_map.get_valid_neighbours(current)

        for neighbour in neighbours:
            if neighbour not in distances:
                queue.append(neighbour)
                distances[neighbour] = distances[current] + 1

    print('Steps:', distances[height_map.end])


def read_height_map():
    with open('12/input.txt', encoding='ascii') as file:
        return HeightMap.from_input_lines(file.readlines())


if __name__ == '__main__':
    main()
