from io import TextIOWrapper
from pickletools import int4
import sys
from typing import Iterable, Iterator


class Reveal:
    MAX_RED: int = 12
    MAX_GREEN: int = 13
    MAX_BLUE: int = 14

    def __init__(self, red: int = 0, green: int = 0, blue: int = 0):
        self.red = red
        self.green = green
        self.blue = blue

    def is_possible(self) -> bool:
        return self.red <= self.MAX_RED and self.green <= self.MAX_GREEN and self.blue <= self.MAX_BLUE

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Reveal):
            return False
        return self.red == __value.red \
            and self.green == __value.green\
            and self.blue == __value.blue

    def __hash__(self) -> int:
        return self.MAX_RED * self.red + self.MAX_GREEN * self.green + self.MAX_BLUE * self.blue


class Game:
    def __init__(self, reveals: set[Reveal]):
        self.reveals = reveals

    def is_possible(self) -> bool:
        return all([reveal.is_possible() for reveal in self.reveals])

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Game):
            return False
        if len(self.reveals) != len(__value.reveals):
            return False
        for reveal in __value.reveals:
            if reveal not in self.reveals:
                return False
        return True


def get_minumum_power_or_game(line: str) -> int:
    _, reveal_lines = line.split(":")
    reveals = reveal_lines.split(";")

    red: int = 0
    green: int = 0
    blue: int = 0

    for reveal in reveals:
        singles = reveal.split(",")
        for take in singles:
            number, color = take.split()
            number = int(number)
            if color == "red" and red < number:
                red = number
            if color == "green" and green < number:
                green = number
            if color == "blue" and blue < number:
                blue = number

    return red * green * blue


def sum_power_minimum(file: Iterable[str]) -> int:
    count: int = 0
    for line in file:
        game = get_minumum_power_or_game(line)
        count += game
    return count


def main(filename: str):
    with open(filename, 'r') as file:
        print(sum_power_minimum(file))


if __name__ == '__main__':
    main(sys.argv[1])
