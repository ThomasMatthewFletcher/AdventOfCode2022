from dataclasses import dataclass
from functools import cache
import re

@dataclass
class Valve:
    name: str
    flow_rate: int
    tunnels: list[str]

class TunnelGraph:
    edges: dict[str, set[str]]

    def __init__(self):
        self.edges = {}

    def add_edge(self, node1: str, node2: str):
        if node1 not in self.edges:
            self.edges[node1] = set()

        if node2 not in self.edges:
            self.edges[node2] = set()

        self.edges[node1].add(node2)
        self.edges[node2].add(node1)

    @cache
    def shortest_dist(self, start: str, end: str) -> int | None:
        explored = set(start)
        distances = {start: 0}
        queue = [start]

        while queue:
            node = queue.pop(0)

            if node == end:
                return distances[node]

            for neighbour in self.edges[node]:
                if neighbour not in explored:
                    explored.add(neighbour)
                    distances[neighbour] = distances[node] + 1
                    queue.append(neighbour)

        return None



def main():
    valves = read_valves()
    tunnel_graph = create_tunnel_graph(valves)

    working_valves = [v for v in valves if v.flow_rate > 0]

    most_pressure = get_most_pressure(30, working_valves, 'AA', tunnel_graph)
    print('Most pressure:', most_pressure)


def get_most_pressure(time_remaining: int, valves: list[Valve], current_valve: str, tunnel_graph: TunnelGraph) -> int:
    remaining_valves = [v for v in valves if v.name != current_valve]
    max_most_pressure = 0

    for valve in remaining_valves:
        valve_name = valve.name
        dist = tunnel_graph.shortest_dist(current_valve, valve_name) + 1

        if dist >= time_remaining:
            continue

        this_valve_pressure = (time_remaining - dist) * valve.flow_rate
        other_pressure = get_most_pressure(time_remaining - dist, remaining_valves, valve.name, tunnel_graph)
        total_pressure = this_valve_pressure + other_pressure

        if total_pressure > max_most_pressure:
            max_most_pressure = total_pressure

    return max_most_pressure


def create_tunnel_graph(valves: list[Valve]) -> TunnelGraph:
    tunnel_graph = TunnelGraph()

    for valve in valves:
        for tunnel in valve.tunnels:
            tunnel_graph.add_edge(valve.name, tunnel)

    return tunnel_graph

def read_valves() -> list[Valve]:
    with open('16/input.txt', encoding='ascii') as file:
        return [parse_valve(line) for line in file]

def parse_valve(line: str) -> Valve:
    match = re.match(r'Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)', line)
    name = match.group(1)
    flow_rate = int(match.group(2))
    tunnels = match.group(3).split(', ')
    return Valve(name, flow_rate, tunnels)

if __name__ == '__main__':
    main()
