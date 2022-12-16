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


@dataclass(frozen=True)
class State:
    time_remaining: int
    valves_remaining: set[str]
    human_to: str
    human_steps_left: int
    elephant_to: str
    elephant_steps_left: int


def main():
    valves = read_valves()
    tunnel_graph = create_tunnel_graph(valves)

    valve_flow_rates = {v.name: v.flow_rate for v in valves if v.flow_rate > 0}

    start_valve = 'AA'

    start_state = State(
        time_remaining=26,
        valves_remaining={v for v in valve_flow_rates.keys() if v != start_valve},
        human_to=start_valve,
        human_steps_left=0,
        elephant_to=start_valve,
        elephant_steps_left=0
    )

    most_pressure = get_most_pressure(start_state, valve_flow_rates, tunnel_graph)
    print('Most pressure:', most_pressure)


def get_most_pressure(state: State, valve_flow_rates: dict[str, int], tunnel_graph: TunnelGraph) -> tuple[int, list[str]]:
    if state.human_steps_left != 0 and state.elephant_steps_left != 0:
        next_state = State(
            time_remaining=state.time_remaining - 1,
            valves_remaining=state.valves_remaining,
            human_to=state.human_to,
            human_steps_left=state.human_steps_left - 1,
            elephant_to=state.elephant_to,
            elephant_steps_left=state.elephant_steps_left - 1
        )
        return get_most_pressure(next_state, valve_flow_rates, tunnel_graph)

    max_most_pressure = 0

    for valve in state.valves_remaining:
        if state.human_steps_left == 0:
            dist = tunnel_graph.shortest_dist(state.human_to, valve) + 1
        else:
            dist = tunnel_graph.shortest_dist(state.elephant_to, valve) + 1

        if dist >= state.time_remaining:
            continue

        this_valve_pressure = (state.time_remaining - dist) * valve_flow_rates[valve]

        if state.human_steps_left == 0:
            next_state = State(
                time_remaining=state.time_remaining,
                valves_remaining=state.valves_remaining - {valve},
                human_to=valve,
                human_steps_left=dist,
                elephant_to=state.elephant_to,
                elephant_steps_left=state.elephant_steps_left
            )
        else:
            next_state = State(
                time_remaining=state.time_remaining,
                valves_remaining=state.valves_remaining - {valve},
                human_to=state.human_to,
                human_steps_left=state.human_steps_left,
                elephant_to=valve,
                elephant_steps_left=dist
            )

        other_pressure = get_most_pressure(next_state, valve_flow_rates, tunnel_graph)
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
