
def main():
    grid = read_grid()
    visible_trees = count_visible_trees(grid)

    print('Visible trees:', visible_trees)

def count_visible_trees(grid: list[list[int]]):
    visible_trees = 0

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if is_tree_visible(grid, x, y):
                visible_trees += 1

    return visible_trees

def is_tree_visible(grid: list[list[int]], x: int, y: int):
    this_height = grid[y][x]

    trees_west  = grid[y][:x]
    trees_east  = grid[y][x+1:]
    trees_north = [row[x] for row in grid[:y]]
    trees_south = [row[x] for row in grid[y+1:]]

    return (
        all(tree < this_height for tree in trees_west) or
        all(tree < this_height for tree in trees_east) or
        all(tree < this_height for tree in trees_north) or
        all(tree < this_height for tree in trees_south)
    )


def read_grid():
    with open('08/input.txt', encoding='ascii') as file:
        return [[int(cell) for cell in line.strip()] for line in file]

if __name__ == '__main__':
    main()
