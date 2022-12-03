
from enum import Enum
from typing import NamedTuple


class Move(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

class Outcome(Enum):
    LOSE = 0
    DRAW = 3
    WIN = 6

class Round(NamedTuple):
    move: Move
    outcome: Outcome

def main():
    rounds = read_rounds()
    score = 0

    for rnd in rounds:
        move = get_round_move(rnd)
        score += move.value + 1 + rnd.outcome.value

    print('Total score:', score)

def get_round_move(rnd: Round):
    if rnd.outcome == Outcome.DRAW:
        return rnd.move

    if rnd.outcome == Outcome.WIN:
        return Move((rnd.move.value+1)%3)

    return Move((rnd.move.value-1)%3)

def read_rounds() -> list[Round]:
    with open('02/input.txt', encoding='utf-8') as file:
        return [Round(char_to_move(line[0]), char_to_outcome(line[2])) for line in file]

def char_to_move(char: str):
    if char == 'A':
        return Move.ROCK
    if char in 'B':
        return Move.PAPER
    if char in 'C':
        return Move.SCISSORS

    raise Exception(f'Invalid move: {char}')

def char_to_outcome(char: str):
    if char == 'X':
        return Outcome.LOSE
    if char == 'Y':
        return Outcome.DRAW
    if char == 'Z':
        return Outcome.WIN
    
    raise Exception(f'Invalid outcome: {char}')

if __name__ == '__main__':
    main()
