NORTH_SOUTH: str = "|"  # is a vertical pipe connecting north and south.
EAST_WEST: str = "-"  # is a horizontal pipe connecting east and west.
NORTH_EAST: str = "L"  # is a 90-degree bend connecting north and east.
NORTH_WEST: str = "J"  # is a 90-degree bend connecting north and west.
SOUTH_WEST: str = "7"  # is a 90-degree bend connecting south and west.
SOUTH_EAST: str = "F"  # is a 90-degree bend connecting south and east.

FLOOR: str = "."  # is ground; there is no pipe in this tile.

ANIMAL: str = "S"


def get_loop(matrix: list[list[str]]) -> list[tuple[int, int]]:
    position_loop: list[tuple[int, int]] = []
    symbol_loop: list[str] = []

    animal_position: tuple[int] = (0, 0)
    for i, row in enumerate(matrix):
        if ANIMAL in row:
            j: int = row.index(ANIMAL)
            animal_position = (i, j)
            break

    position_loop.append(animal_position)
    symbol_loop.append(ANIMAL)

    current_position: tuple[int, int]
    current_symbol: str

    if animal_position[0] > 0 and matrix[animal_position[0] - 1][animal_position[1]] in [SOUTH_EAST, SOUTH_WEST, NORTH_SOUTH]:
        current_position = (animal_position[0] - 1, animal_position[1])
    elif animal_position[0] < len(matrix) - 1 and matrix[animal_position[0] + 1][animal_position[1]] in [NORTH_EAST, NORTH_SOUTH, NORTH_WEST]:
        current_position = (animal_position[0] + 1, animal_position[1])
    elif animal_position[1] > 0 and matrix[animal_position[0]][animal_position[1] - 1] in [EAST_WEST, NORTH_EAST, SOUTH_EAST]:
        current_position = (animal_position[0], animal_position[1] - 1)
    elif animal_position[1] < len(matrix[0]) and matrix[animal_position[0]][animal_position[1] + 1] in [EAST_WEST, NORTH_WEST, SOUTH_WEST]:
        current_position = (animal_position[0], animal_position[1] + 1)

    current_symbol = matrix[current_position[0]][current_position[1]]

    position_loop.append(current_position)
    symbol_loop.append(current_symbol)

    while current_symbol != ANIMAL:
        previous_position: tuple[int, int] = position_loop[-2]
        if current_symbol == NORTH_SOUTH:
            if previous_position[0] + 1 == current_position[0]:
                current_position = (
                    current_position[0] + 1, current_position[1])
            else:
                current_position = (
                    current_position[0] - 1, current_position[1])
        elif current_symbol == EAST_WEST:
            if previous_position[1] + 1 == current_position[1]:
                current_position = (
                    current_position[0], current_position[1] + 1)
            else:
                current_position = (
                    current_position[0], current_position[1] - 1)
        elif current_symbol == NORTH_EAST:
            if previous_position[0] + 1 == current_position[0]:
                current_position = (
                    current_position[0], current_position[1] + 1)
            else:
                current_position = (
                    current_position[0] - 1, current_position[1])
        elif current_symbol == NORTH_WEST:
            if previous_position[0] + 1 == current_position[0]:
                current_position = (
                    current_position[0], current_position[1] - 1)
            else:
                current_position = (
                    current_position[0] - 1, current_position[1])
        elif current_symbol == SOUTH_WEST:
            if previous_position[0] - 1 == current_position[0]:
                current_position = (
                    current_position[0], current_position[1]-1)
            else:
                current_position = (
                    current_position[0]+1, current_position[1])
        elif current_symbol == SOUTH_EAST:
            if previous_position[0] - 1 == current_position[0]:
                current_position = (
                    current_position[0], current_position[1] + 1)
            else:
                current_position = (
                    current_position[0] + 1, current_position[1])

        current_symbol = matrix[current_position[0]][current_position[1]]
        position_loop.append(current_position)
        symbol_loop.append(current_symbol)

    return position_loop


def parse_matrix(file_name: str) -> list[list[str]]:
    matrix: list[list[str]] = []
    with open(file_name, "r") as file:
        for line in file.readlines():
            line = line.strip("\n")
            matrix.append(list(line))
    return matrix


def get_max_step(file_name: str) -> int:
    matrix: list[list[str]] = parse_matrix(file_name)
    loop: list[str] = get_loop(matrix)
    return len(loop) // 2


def count_inside(matrix: list[list[str]]) -> int:
    result: int = 0

    for row in matrix:
        should_count: bool = False
        for element in row:
            if element in [NORTH_SOUTH, SOUTH_EAST, SOUTH_WEST]:
                should_count = not should_count
            elif should_count and element == '.':
                result += 1

    return result


def get_number_inside(file_name: str) -> int:
    matrix: list[list[str]] = parse_matrix(file_name)
    loop: list[tuple[int, int]] = get_loop(matrix)

    matrix_with_only_loop: list[list[str]] = [
        ["." for _ in matrix[0]]
        for _ in matrix
    ]

    for i, row in enumerate(matrix):
        for j, element in enumerate(row):
            if element == ANIMAL:
                first: tuple[int, int] = loop[1]
                last: tuple[int, int] = loop[-2]
                if first[0] > i:
                    if last[0] < i:
                        matrix_with_only_loop[i][j] = NORTH_SOUTH
                    elif last[1] < j:
                        matrix_with_only_loop[i][j] = SOUTH_WEST
                    else:
                        matrix_with_only_loop[i][j] = SOUTH_EAST
                elif last[0] > i:
                    if first[0] < i:
                        matrix_with_only_loop[i][j] = NORTH_SOUTH
                    elif first[1] < j:
                        matrix_with_only_loop[i][j] = SOUTH_WEST
                    elif first[1] > j:
                        matrix_with_only_loop[i][j] = SOUTH_EAST
                else:
                    matrix_with_only_loop[i][j] = ANIMAL

            elif (i, j) in loop:
                matrix_with_only_loop[i][j] = element

    return count_inside(matrix_with_only_loop)


def main(file_name: str = "./10/input.txt"):
    print(get_number_inside(file_name))


if __name__ == "__main__":
    main()
