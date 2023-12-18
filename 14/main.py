import functools
from typing import Iterable, final


ROUND_ROCK = "O"
SQUARE_ROCK = "#"
EMPTY = "."


def tilt(line: str) -> str:
    result: list[str] = []
    number_of_empty: int = 0
    number_of_round_rocks: int = 0

    for cell in line:
        if cell == EMPTY:
            number_of_empty += 1
        elif cell == ROUND_ROCK:
            number_of_round_rocks += 1
        elif cell == SQUARE_ROCK:
            result.extend(ROUND_ROCK * number_of_round_rocks)
            number_of_round_rocks = 0
            result.extend(EMPTY * number_of_empty)
            number_of_empty = 0
            result.append(SQUARE_ROCK)
        else:
            raise Exception(f"Unknown cell: {cell}")

    result.extend(ROUND_ROCK * number_of_round_rocks)
    result.extend(EMPTY * number_of_empty)

    return "".join(result)


def tilt_dish_north(dish: list[str]) -> list[str]:
    tilted_columns: list[str] = [
        tilt("".join(line[k] for line in dish))
        for k in range(len(dish[0]))
    ]
    result = [
        "".join([line[k] for line in tilted_columns])
        for k in range(len(tilted_columns[0]))
    ]
    return result


def tilt_dish_west(dish: list[str]) -> list[str]:
    return [
        tilt(str(line))
        for line in dish
    ]


def tilt_dish_south(dish: list[str]) -> list[str]:
    transposed: list[str] = [
        "".join(line[k] for line in dish[::-1])
        for k in range(len(dish[0]))
    ]
    tilted_columns: list[str] = [
        tilt(str(line))
        for line in transposed
    ]
    result = [
        "".join([line[k] for line in tilted_columns])
        for k in range(len(tilted_columns[0]))[::-1]
    ]
    return result


def tilt_dish_east(dish: list[str]) -> list[str]:
    tilted_columns: list[str] = [
        tilt(line[::-1])
        for line in dish
    ]
    result = [
        line[::-1]
        for line in tilted_columns
    ]
    return result


def tilt_dish_cycle(dish: list[str]) -> list[str]:
    tilted_north = tilt_dish_north(dish)
    tilted_west = tilt_dish_west(tilted_north)
    tilted_south = tilt_dish_south(tilted_west)
    tilted_east = tilt_dish_east(tilted_south)
    return tilted_east


def get_total_load(dish: list[str]) -> int:
    max_points: int = len(dish)
    total_load: int = sum(
        dish[i].count(ROUND_ROCK) * (max_points - i)
        for i in range(len(dish))
    )
    return total_load


def compute_total_load(file_name: str) -> int:
    dish: list[str] = []
    with open(file_name, "r") as file:
        dish = [line.strip("\n") for line in file.readlines()]

    seen: list[list[str]] = [dish.copy()]

    cycle_start: int = 0
    cycle_length: int = 0
    for i in range(1000000000):
        tilted_dish = tilt_dish_cycle(seen[-1])
        if tilted_dish in seen:
            cycle_start = seen.index(tilted_dish)
            cycle_length = i - cycle_start + 1
            break
        seen.append(tilted_dish)

    print(f"Cycle start: {cycle_start}")
    print(f"Cycle length: {cycle_length}")

    tilted_dish: list[str] = dish.copy()

    after_cycle: int = (1000000000 - cycle_start) % cycle_length
    for i in range(cycle_start + after_cycle):
        tilted_dish = tilt_dish_cycle(tilted_dish)

    total_load = get_total_load(tilted_dish)

    return total_load


if __name__ == '__main__':
    total_load: int = compute_total_load("./14/input.txt")
    print(f"Total load: {total_load}")
