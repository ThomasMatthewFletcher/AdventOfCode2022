
DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

class Grid:
    cells: list[list[int]]
    width: int
    height: int

    def __init__(self, cells: list[list[int]]):
        self.cells = cells
        self.width = len(cells[0])
        self.height = len(cells)

    def get_max_scenic_score(self):
        max_scenic_score = 0

        for y in range(self.height):
            for x in range(self.width):
                scenic_score = self.get_scenic_score(x, y)
                max_scenic_score = max(max_scenic_score, scenic_score)

        return max_scenic_score

    def get_scenic_score(self, x: int, y: int):
        viewing_distances = 1

        for direction in DIRECTIONS:
            viewing_distances *= self.get_viewing_distance(x, y,  direction[0], direction[1])

        return viewing_distances

    def get_viewing_distance(self, x: int, y: int, dx: int, dy: int):
        this_height = self.cells[y][x]
        x += dx
        y += dy

        viewing_distance = 0

        while x >= 0 and x < self.width and y >= 0 and y < self.height:
            viewing_distance += 1

            if self.cells[y][x] >= this_height:
                break

            x += dx
            y += dy

        return viewing_distance


def main():
    grid = read_grid()
    print(grid.get_max_scenic_score())


def read_grid():
    with open('08/input.txt', encoding='ascii') as file:
        return Grid([[int(cell) for cell in line.strip()] for line in file])

if __name__ == '__main__':
    main()
