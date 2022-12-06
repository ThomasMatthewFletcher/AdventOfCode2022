MARKER_SIZE = 14

def main():
    datastream = read_datastream()
    print('Start marker:', find_start_marker(datastream))

def find_start_marker(datastream: str):
    for i in range(len(datastream) - MARKER_SIZE + 1):
        unique_chars = len(set(datastream[i:i+MARKER_SIZE]))
        if unique_chars == MARKER_SIZE:
            return i + MARKER_SIZE


def read_datastream():
    with open('06/input.txt', encoding='ascii') as file:
        return file.readline().strip()

if __name__ == '__main__':
    main()
