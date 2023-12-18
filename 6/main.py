from functools import reduce


def get_ways_to_win(time: int, distance: int) -> list[int]:
    result: list[int] = []
    for i in range(time + 1):
        speed: int = i
        distance_traveled: int = speed * (time - i)
        if distance < distance_traveled:
            result.append(i)
    return result


def get_number_of_ways(file: str) -> int:
    lines: list[str] = file.split("\n")
    time: int = int(lines[0].split(':')[1].replace(' ', ''))
    distance: int = int(lines[1].split(':')[1].replace(' ', ''))
    return len(get_ways_to_win(time, distance))


def main(filename: str = "./6/input.txt"):
    with open(filename) as file:
        print(get_number_of_ways(file.read()))


if __name__ == "__main__":
    main()
