
from enum import Enum
from typing import Tuple


class Move(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

Round = Tuple[Move, Move]

class Outcome(Enum):
    LOSE = 0
    DRAW = 3
    WIN = 6


def main():
    rounds = read_rounds()
    score = 0

    for rnd in rounds:
        outcome = get_round_outcome(rnd)
        score += rnd[1].value + outcome.value

    print('Total score:', score)

def get_round_outcome(rnd: Round):
    move1, move2 = rnd

    if move1 == move2:
        return Outcome.DRAW

    if move1 == Move.ROCK and move2 == Move.PAPER:
        return Outcome.WIN

    if move1 == Move.PAPER and move2 == Move.SCISSORS:
        return Outcome.WIN

    if move1 == Move.SCISSORS and move2 == Move.ROCK:
        return Outcome.WIN

    return Outcome.LOSE

def read_rounds() -> list[Round]:
    with open('02/input.txt', encoding='utf-8') as file:
        return [(char_to_move(line[0]), char_to_move(line[2])) for line in file]

def char_to_move(char):
    if char in 'AX':
        return Move.ROCK
    if char in 'BY':
        return Move.PAPER
    if char in 'CZ':
        return Move.SCISSORS

    raise Exception(f'Invalid move: {char}')



if __name__ == '__main__':
    main()
