import math
import sys
from timeit import repeat

INSTRUCTIONS: dict[str, int] = {
    "L": 0,
    "R": 1,
}


def get_first_steps(desert_map: dict[str, tuple[str, str]]) -> list[str]:
    return [step for step in desert_map if step[-1] == "A"]


def are_last_steps(current_steps: list[str]) -> bool:
    for step in current_steps:
        if step[-1] != "Z":
            return False
    return True


def get_number_of_steps(desert_map: dict[str, tuple[str, str]], instructions: str) -> int:
    current_steps: list[str] = get_first_steps(desert_map)

    number_of_steps: int = 0
    len_instrunctions = len(instructions)

    tmp: list[str] = current_steps.copy()
    number_of_steps_before_end: list[int] = [0] * len(current_steps)
    for i, step in enumerate(current_steps):
        number: int = 0
        while tmp[i][-1] != "Z":
            instruction = INSTRUCTIONS[
                instructions[number % len_instrunctions]
            ]
            tmp[i] = desert_map[tmp[i]][instruction]
            number += 1
        number_of_steps_before_end[i] = number

    print(number_of_steps_before_end)

    number_of_steps = math.lcm(*number_of_steps_before_end)

    return number_of_steps


def parse_map_line(line: str) -> tuple[str, tuple[str, str]]:
    left, right = line.split(" = ")

    source: str = left.strip()
    split_destination: list[str] = right.strip("()\n").split(", ")
    destination: tuple[str, str] = (split_destination[0], split_destination[1])

    return (source, destination)


def get_steps(file_name: str) -> int:
    instructions: str
    desert_map: dict[str, tuple[str, str]] = {}

    with open(file_name, "r") as file:
        instructions = file.readline().replace("\n", '')
        file.readline()

        for line in file.readlines():
            source, destination = parse_map_line(line)
            desert_map[source] = destination

    return get_number_of_steps(desert_map, instructions)


def main(file_name: str = "./8/input.txt"):
    print(get_steps(file_name))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
