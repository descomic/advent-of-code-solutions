def expand_universe(universe: list[list[str]]) -> tuple[list[int], list[int]]:
    empty_rows: list[int] = []
    empty_colums: list[int] = list(range(len(universe[0])))
    for i, row in enumerate(universe):
        if '#' not in row:
            empty_rows.append(i)
        for j, cell in enumerate(row):
            if cell == '#' and j in empty_colums:
                empty_colums.remove(j)
    return empty_rows, empty_colums


def sum_of_shortest_paths(universe: list[list[str]], expansion_rate: int = 1_000_000) -> int:
    empty_rows, empty_columns = expand_universe(universe)

    galaxies: list[tuple[int, int]] = []
    for i, row in enumerate(universe):
        for j, cell in enumerate(row):
            if cell == '#':
                galaxies.append((i, j))

    length_of_paths: list[int] = []
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            max_row: int = max(galaxies[i][0], galaxies[j][0])
            min_row: int = min(galaxies[i][0], galaxies[j][0])
            max_column: int = max(galaxies[i][1], galaxies[j][1])
            min_column: int = min(galaxies[i][1], galaxies[j][1])
            row_expansion: int = (expansion_rate - 1) * \
                len(list(filter(lambda row_index: min_row <
                    row_index < max_row, empty_rows)))
            column_expansion: int = (expansion_rate - 1) * \
                len(list(filter(lambda column_index: min_column <
                    column_index < max_column, empty_columns)))

            row_distance: int = abs(
                galaxies[i][0] - galaxies[j][0]
            ) + row_expansion
            column_distance: int = abs(
                galaxies[i][1] - galaxies[j][1]
            ) + column_expansion
            length_of_paths.append(row_distance + column_distance)
    return sum(length_of_paths)


def parse_universe(file: str) -> list[list[str]]:
    universe: list[list[str]] = []
    for line in file.splitlines():
        universe.append(list(line))
    return universe


def get_sum_shortest_paths(file_name: str) -> int:
    universe: list[list[str]]
    with open(file_name, 'r') as file:
        universe = parse_universe(file.read())
    return sum_of_shortest_paths(universe)


def main(file_name: str = './11/input.txt'):
    print(get_sum_shortest_paths(file_name))


if __name__ == '__main__':
    main()
