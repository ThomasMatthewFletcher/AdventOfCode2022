from functools import cache
from typing import NamedTuple
import re
import heapq

DURATION = 32

class Stock(NamedTuple):
    ore: int
    clay: int
    obsidian: int
    geode: int

class RobotCosts(NamedTuple):
    ore: Stock
    clay: Stock
    obsidian: Stock
    geode: Stock

class Blueprint(NamedTuple):
    id: int
    robot_costs: RobotCosts

class State(NamedTuple):
    material_stock: Stock
    robot_stock: Stock

def get_max_geodes(blueprint: Blueprint) -> int:

    initial_state = State(
        material_stock = Stock(0, 0, 0, 0),
        robot_stock = Stock(1, 0, 0, 0)
    )

    queue = [(0, initial_state)]
    heapq.heapify(queue)

    seen_states = {initial_state}
    dist = {initial_state: 0}

    max_geodes = 0

    while queue:
        _, state = heapq.heappop(queue)

        if dist[state] == DURATION:

            if state.material_stock.geode > max_geodes:
                max_geodes = state.material_stock.geode
        else:
            remaining_dist = DURATION - dist[state]

            max_remaining_collection = triangle_number(remaining_dist - 1)

            max_obsidian = state.material_stock.obsidian + (state.robot_stock.obsidian * remaining_dist) + max_remaining_collection
            max_geode_robot_purchases = min(max_obsidian // blueprint.robot_costs.geode.obsidian, remaining_dist - 1)

            max_geode_collection = triangle_number(max_geode_robot_purchases)

            max_possible_geodes = max_geode_collection + state.material_stock.geode + (state.robot_stock.geode * remaining_dist)

            if max_possible_geodes > max_geodes:
                next_states = get_next_states(state, blueprint)
                for next_state in next_states:
                    this_dist = dist[state] + 1
                    if next_state not in seen_states or this_dist < dist[next_state]:
                        heapq.heappush(queue, ((
                            -next_state.material_stock.geode * 100
                            -next_state.material_stock.obsidian
                        ), next_state))
                        seen_states.add(next_state)
                        dist[next_state] = this_dist

    return max_geodes

@cache
def triangle_number(n: int) -> int:
    return n * (n + 1) // 2

def is_stock_enough(stock: Stock, cost: Stock):
    for val1, val2 in zip(stock, cost):
        if val1 < val2:
            return False
    return True

def get_next_states(state: State, blueprint: Blueprint) -> list[State]:
    next_states: list[State] = []

    next_stock = Stock(
        state.material_stock.ore + state.robot_stock.ore,
        state.material_stock.clay + state.robot_stock.clay,
        state.material_stock.obsidian + state.robot_stock.obsidian,
        state.material_stock.geode + state.robot_stock.geode
    )

    # Do nothing state
    next_states.append(State(
        material_stock = next_stock,
        robot_stock = state.robot_stock
    ))

    # State for creating each robot type
    for robot_index, robot_cost in enumerate(blueprint.robot_costs):
        if is_stock_enough(state.material_stock, robot_cost):
            stock_list = list(state.robot_stock)
            stock_list[robot_index] += 1

            next_states.append(State(
                material_stock = Stock(
                    next_stock.ore - robot_cost.ore,
                    next_stock.clay - robot_cost.clay,
                    next_stock.obsidian - robot_cost.obsidian,
                    next_stock.geode - robot_cost.geode
                ),
                robot_stock = Stock(*stock_list)
            ))

    return next_states


def main():
    blueprints = read_blueprints()[:3]
    geode_mult = 1

    for blueprint in blueprints:
        max_geodes = get_max_geodes(blueprint)
        print(f'Blueprint {blueprint.id} max geodes: {max_geodes}')
        geode_mult *= max_geodes

    print('Geodes Multiplied:', geode_mult)

def read_blueprints() -> list[Blueprint]:
    with open('19/input.txt', encoding='ascii') as file:
        return [parse_blueprint(line) for line in file]

def parse_blueprint(line: str) -> Blueprint:
    matches = list(map(int, re.findall(r'\d+', line)))
    return Blueprint(
        id = matches[0],
        robot_costs = RobotCosts(
            ore      = Stock(matches[1], 0, 0, 0),
            clay     = Stock(matches[2], 0, 0, 0),
            obsidian = Stock(matches[3], matches[4], 0, 0),
            geode    = Stock(matches[5], 0, matches[6], 0)
        )
    )

if __name__ == '__main__':
    main()
