EMPTY_SPACE: str = "."
FORWARD_SLASH_MIRROR: str = "/"
BACKWARD_SLASH_MIRROR: str = "\\"
VERTICAL_SPLITTER: str = "|"
HORIZONTAL_SPLITTER: str = "-"

ENERGIZED: str = "#"

UPWARD: tuple[int, int] = (-1, 0)
DOWNWARD: tuple[int, int] = (1, 0)
LEFTWARD: tuple[int, int] = (0, -1)
RIGHTWARD: tuple[int, int] = (0, 1)

UPWARD_ARROW: str = "^"
DOWNWARD_ARROW: str = "v"
LEFTWARD_ARROW: str = "<"
RIGHTWARD_ARROW: str = ">"

DIRECTION_TO_ARROW: dict[tuple[int, int], str] = {
    UPWARD: UPWARD_ARROW,
    DOWNWARD: DOWNWARD_ARROW,
    LEFTWARD: LEFTWARD_ARROW,
    RIGHTWARD: RIGHTWARD_ARROW,
}


def pass_beam_through(grid: list[str], current_row: int, current_column: int, next_row_direction: int, next_column_direction: int,) -> int:
    already_seen: set[tuple[int, int]] = set()

    no_loop: bool = True
    to_do: list[tuple[int, int, int, int]] = []

    while no_loop:
        if current_row < 0 or len(grid) <= current_row or current_column < 0 or len(grid[0]) <= current_column:
            if to_do:
                tmp: tuple[int, int, int, int] = to_do.pop()
                current_row = tmp[0]
                current_column = tmp[1]
                next_row_direction = tmp[2]
                next_column_direction = tmp[3]
                continue
            else:
                no_loop = False
                break

        current_tile: str = grid[current_row][current_column]
        already_seen.add((current_row, current_column))

        if current_tile == EMPTY_SPACE or current_tile in DIRECTION_TO_ARROW.values() or current_tile.isnumeric():
            if current_tile == DIRECTION_TO_ARROW.get((next_row_direction, next_column_direction)):
                if to_do:
                    tmp: tuple[int, int, int, int] = to_do.pop()
                    current_row = tmp[0]
                    current_column = tmp[1]
                    next_row_direction = tmp[2]
                    next_column_direction = tmp[3]
                    continue
                else:
                    no_loop = False
                    break

            new_value: str
            if current_tile == EMPTY_SPACE:
                new_value = DIRECTION_TO_ARROW.get(
                    (next_row_direction, next_column_direction))
            elif current_tile in DIRECTION_TO_ARROW.values():
                new_value = "2"
            else:
                new_value = str(int(grid[current_row][current_column]) + 1) if int(
                    grid[current_row][current_column]) < 4 else "4"
            grid[current_row] = grid[current_row][:current_column] + \
                new_value + grid[current_row][current_column + 1:]

            current_row += next_row_direction
            current_column += next_column_direction

        elif current_tile == HORIZONTAL_SPLITTER:
            if (next_row_direction, next_column_direction) == RIGHTWARD or (next_row_direction, next_column_direction) == LEFTWARD:
                current_row += next_row_direction
                current_column += next_column_direction
            else:
                to_do.append(tuple([current_row, current_column + 1, 0, 1]))
                current_column -= 1
                next_row_direction = 0
                next_column_direction = -1

        elif current_tile == VERTICAL_SPLITTER:
            if (next_row_direction, next_column_direction) == UPWARD or (next_row_direction, next_column_direction) == DOWNWARD:
                current_row += next_row_direction
                current_column += next_column_direction
            else:
                to_do.append(tuple([current_row + 1, current_column, 1, 0]))
                current_row -= 1
                next_row_direction = -1
                next_column_direction = 0

        elif current_tile == FORWARD_SLASH_MIRROR:
            if next_column_direction == 1:
                next_row_direction = -1
                next_column_direction = 0
            elif next_column_direction == -1:
                next_row_direction = 1
                next_column_direction = 0
            elif next_row_direction == 1:
                next_row_direction = 0
                next_column_direction = -1
            elif next_row_direction == -1:
                next_row_direction = 0
                next_column_direction = 1
            current_row += next_row_direction
            current_column += next_column_direction

        elif current_tile == BACKWARD_SLASH_MIRROR:
            if next_column_direction == 1:
                next_row_direction = 1
                next_column_direction = 0
            elif next_column_direction == -1:
                next_row_direction = -1
                next_column_direction = 0
            elif next_row_direction == -1:
                next_row_direction = 0
                next_column_direction = -1
            elif next_row_direction == 1:
                next_row_direction = 0
                next_column_direction = 1
            current_row += next_row_direction
            current_column += next_column_direction

        else:
            raise ValueError("WTF")

    return len(already_seen)


def get_best_number_of_energized_tiles(file_name: str) -> int:
    grid: list[str]
    with open(file_name, "r") as file:
        grid = file.read().splitlines()

    results: list[int] = []
    for i in range(len(grid)):
        results.append(pass_beam_through(grid.copy(), i, 0, 0, 1))
        results.append(pass_beam_through(
            grid.copy(), i, len(grid[0]) - 1, 0, -1))
    for i in range(len(grid[0])):
        results.append(pass_beam_through(grid.copy(), 0, i, 1, 0))
        results.append(pass_beam_through(grid.copy(), len(grid) - 1, i, -1, 0))
    return max(results)


if __name__ == '__main__':
    print(get_best_number_of_energized_tiles("./16/input.txt"))
