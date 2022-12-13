import functools
from typing import Union

Packet = list[Union[int, 'Packet']]


def main():
    packets = read_packets()
    packets.append([[2]])
    packets.append([[6]])

    packets.sort(key=functools.cmp_to_key(compare_packets))

    decoder_key = (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)
    print('Decoder key:', decoder_key)


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

def read_packets():
    with open('13/input.txt', encoding='ascii') as file:
        return [parse_packet(list(line.strip())) for line in file if line.strip()]

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
