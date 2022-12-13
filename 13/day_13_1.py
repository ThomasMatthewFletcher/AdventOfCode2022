from typing import Union

Packet = list[Union[int, 'Packet']]


def main():
    packet_pairs = read_packet_pairs()

    sum_indices = 0

    for i, packet_pair in enumerate(packet_pairs):
        result = compare_packets(packet_pair[0], packet_pair[1])

        if result == -1:
            sum_indices += i + 1

    print('Sum indices:', sum_indices)


def compare_packets(packet1: Packet, packet2: Packet):
    for value1, value2 in zip(packet1, packet2):
        if isinstance(value1, int) and isinstance(value2, int):
            if value1 < value2:
                return -1
            elif value2 < value1:
                return 1
        elif isinstance(value1, list) and isinstance(value2, list):
            result = compare_packets(value1, value2)
            if result:
                return result
        elif isinstance(value1, list):
            return compare_packets(value1, [value2])
        elif isinstance(value2, list):
            return compare_packets([value1], value2)

    if len(packet1) < len(packet2):
        return -1

    if len(packet2) < len(packet1):
        return 1

    return 0


def read_packet_pairs():
    with open('13/input.txt', encoding='ascii') as file:
        data = file.read()

    chunks = data.split('\n\n')
    packet_pairs: list[tuple[Packet, Packet]] = []

    for chunk in chunks:
        lines = chunk.split('\n')
        packet_pairs.append((
            parse_packet(list(lines[0])),
            parse_packet(list(lines[1]))
        ))

    return packet_pairs

def parse_packet(line: list[str]) -> Packet:
    packet: Packet = []

    if line.pop(0) != '[':
        raise Exception('Invalid packet')

    value = ''

    while line:
        char = line.pop(0)

        match char:
            case '[':
                line.insert(0, '[')
                packet.append(parse_packet(line))
            case ']':
                if value != '':
                    packet.append(int(value))
                return packet
            case ',':
                if value != '':
                    packet.append(int(value))
                value = ''
            case _:
                value += char

    raise Exception('Invalid packet')

if __name__ == '__main__':
    main()
