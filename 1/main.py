import sys

SPELLED_OUT_DIGITS: dict[str, int] = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}


def convert_spelled_out_digits_to_numbers(line: str) -> str:
    new_line: str = str(line)
    done: bool = False
    while not done:
        index_spelled_out_digit: int = len(new_line)
        current_digit: str = ''
        for spelled_out_digit in SPELLED_OUT_DIGITS:
            if spelled_out_digit in new_line:
                current_index = new_line.index(spelled_out_digit)
                if current_index < index_spelled_out_digit:
                    index_spelled_out_digit = current_index
                    current_digit = spelled_out_digit
        if current_digit == '' or index_spelled_out_digit == len(new_line):
            done = True
            break
        new_line = new_line.replace(current_digit,
                                    str(SPELLED_OUT_DIGITS[current_digit]),
                                    1)
    return new_line


def get_first_digit(line: str) -> int:
    bigger: str = ''
    for char in line:
        if char.isdigit():
            return int(char)
        bigger += char
        for spelled_out_digit in SPELLED_OUT_DIGITS:
            if spelled_out_digit in bigger:
                return SPELLED_OUT_DIGITS[spelled_out_digit]
    raise ValueError("No digit found in line")


def get_last_digit(line: str) -> int:
    bigger: str = ''
    for char in line[::-1]:
        if char.isdigit():
            return int(char)
        bigger = char + bigger
        for spelled_out_digit in SPELLED_OUT_DIGITS:
            if spelled_out_digit in bigger:
                return SPELLED_OUT_DIGITS[spelled_out_digit]
    raise ValueError("No digit found in line")


def get_sum_of_calibration_values(lines: list[str]) -> int:
    sum_of_calibration_values: int = 0
    for line in lines:
        first_digit = get_first_digit(line)
        last_digit = get_last_digit(line)
        calibration_value = first_digit * 10 + last_digit
        sum_of_calibration_values += calibration_value
    return sum_of_calibration_values


def main(args: list[str]):
    print()
    print("Advent of Code 2020")
    print("Day 1: Report Repair")
    print()

    with open(args[1]) as f:
        lines = f.readlines()
        print("Sum of calibration values:",
              get_sum_of_calibration_values(lines))


if __name__ == "__main__":
    main(sys.argv)
