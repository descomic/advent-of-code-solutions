import sys


def is_star(character: str) -> bool:
    return character == '*'


def hash_coordinates(x: int, y: int) -> int:
    return x * 1000 + y


def get_sum_of_part_numbers(part_numbers: list[str]) -> int:

    HEIGHT: int = len(part_numbers)
    WIDTH: int = len(part_numbers[0])

    star_repo: dict[int, list[int]] = dict()

    for row_index, row in enumerate(part_numbers):
        ongoing_number: str = ""
        current_stars: set[int] = set()

        for column_index, character in enumerate(row):
            if character.isdigit():
                ongoing_number += character

                if column_index > 0 and is_star(part_numbers[row_index][column_index - 1]):
                    current_stars.add(hash_coordinates(
                        row_index, column_index - 1))
                if column_index < WIDTH - 1 and is_star(part_numbers[row_index][column_index + 1]):
                    current_stars.add(hash_coordinates(
                        row_index, column_index + 1))
                if row_index > 0 and is_star(part_numbers[row_index - 1][column_index]):
                    current_stars.add(hash_coordinates(
                        row_index - 1, column_index))
                if row_index < HEIGHT - 1 and is_star(part_numbers[row_index + 1][column_index]):
                    current_stars.add(hash_coordinates(
                        row_index + 1, column_index))

                if column_index > 0 and row_index > 0 and is_star(part_numbers[row_index - 1][column_index - 1]):
                    current_stars.add(hash_coordinates(
                        row_index - 1, column_index - 1))
                if column_index < WIDTH - 1 and row_index > 0 and is_star(part_numbers[row_index - 1][column_index + 1]):
                    current_stars.add(hash_coordinates(
                        row_index - 1, column_index + 1))
                if column_index > 0 and row_index < HEIGHT - 1 and is_star(part_numbers[row_index + 1][column_index - 1]):
                    current_stars.add(hash_coordinates(
                        row_index + 1, column_index - 1))
                if column_index < WIDTH - 1 and row_index < HEIGHT - 1 and is_star(part_numbers[row_index + 1][column_index + 1]):
                    current_stars.add(hash_coordinates(
                        row_index + 1, column_index + 1))

            else:
                if ongoing_number != "" and len(current_stars) > 0:
                    for symbol in current_stars:
                        if symbol in star_repo:
                            star_repo[symbol].append(int(ongoing_number))
                        else:
                            star_repo[symbol] = [int(ongoing_number)]
                ongoing_number = ""
                current_stars = set()

    count: int = 0
    for star_hash in star_repo:
        if len(star_repo[star_hash]) == 2:
            count += star_repo[star_hash][0] * star_repo[star_hash][1]
    return count


def main(filename: str = "input.txt"):
    with open(filename, "r") as file:
        lines = file.readlines()
        print(get_sum_of_part_numbers(lines))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main("C:\\Users\\michael.descombes\\Documents\\Projects\\advent-of-code\\3\\input.txt")
    main(sys.argv[1])
