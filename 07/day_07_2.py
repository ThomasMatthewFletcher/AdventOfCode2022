from abc import ABC, abstractmethod

TOTAL_SPACE    = 70000000
REQUIRED_SPACE = 30000000

class Item(ABC):
    name: str

    @abstractmethod
    def get_size(self) -> int:
        pass

    @abstractmethod
    def tree(self, depth=0) -> str:
        pass

    def tree_name(self, depth: int) -> str:
        return f'{" " * depth * 2}- {self.name}'

class File(Item):
    name: str
    filesize: int

    def __init__(self, name: str, filesize: int):
        self.name = name
        self.filesize = filesize

    def get_size(self):
        return self.filesize

    def tree(self, depth=0):
        return f'{self.tree_name(depth)} (file, size={self.filesize})\n'

class Directory(Item):
    name: str
    contents: list[Item]

    def __init__(self, name: str):
        self.name = name
        self.contents = []

    def add(self, item: Item):
        self.contents.append(item)

    def get_size(self):
        return sum(item.get_size() for item in self.contents)

    def find_subdirectory(self, name: str):
        return next(item for item in self.contents if item.name == name)

    def tree(self, depth=0):
        part = f'{self.tree_name(depth)} (dir)\n'

        for item in self.contents:
            part += item.tree(depth+1)

        return part

    def find_dirs_lte(self, size: int):
        dirs: list[Directory] = []

        if self.get_size() <= size:
            dirs.append(self)

        for item in self.contents:
            if isinstance(item, Directory):
                dirs.extend(item.find_dirs_lte(size))

        return dirs

    def get_dir_sizes(self):
        sizes: list[int] = [self.get_size()]

        for item in self.contents:
            if isinstance(item, Directory):
                sizes.extend(item.get_dir_sizes())

        return sizes


def main():
    root = Directory('/')
    current_path = [root]

    terminal = read_terminal()

    while terminal:
        line = terminal.pop(0)
        parts = line.split()

        if parts[0] == '$':
            if parts[1] == 'cd':
                if parts[2] == '/':
                    current_path = [root]
                elif parts[2] == '..':
                    current_path.pop()
                else:
                    current_dir = current_path[-1]
                    new_dir = current_dir.find_subdirectory(parts[2])
                    current_path.append(new_dir)
            if parts[1] == 'ls':
                while terminal and not terminal[0].startswith('$'):
                    line = terminal.pop(0)
                    parts = line.split()
                    current_dir = current_path[-1]
                    if parts[0] == 'dir':
                        current_dir.add(Directory(parts[1]))
                    else:
                        current_dir.add(File(parts[1], int(parts[0])))

    current_usage = root.get_size()
    current_free_space = TOTAL_SPACE - current_usage
    min_to_delete = REQUIRED_SPACE - current_free_space

    dir_sizes = root.get_dir_sizes()
    candidate_dir_sizes = [s for s in dir_sizes if s >= min_to_delete]
    candidate_dir_sizes.sort()

    print('Total size of smallest dir:', candidate_dir_sizes[0])



def read_terminal():
    with open('07/input.txt', encoding='ascii') as file:
        return file.readlines()

if __name__ == '__main__':
    main()
