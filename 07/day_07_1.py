from abc import ABC, abstractmethod

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

    dirs = root.find_dirs_lte(100000)
    sum_of_sizes = sum(d.get_size() for d in dirs)
    print('Sum of sizes:', sum_of_sizes)


def read_terminal():
    with open('07/input.txt', encoding='ascii') as file:
        return file.readlines()

if __name__ == '__main__':
    main()
