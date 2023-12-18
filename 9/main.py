from functools import reduce


def get_next_value(history: list[int]) -> int:
    result: int = history[-1]

    current_history: list[int] = history.copy()

    while reduce(lambda i, j: i != 0 or j != 0, current_history):
        current_history = [
            current_history[i + 1] - current_history[i]
            for i in range(len(current_history) - 1)
        ]
        result += current_history[-1]

    return result


def get_previous_value(history: list[int]) -> int:
    current_history: list[int] = history.copy()
    transformation: list[int] = [history[0]]

    while reduce(lambda i, j: i != 0 or j != 0, current_history):
        current_history = [
            current_history[i + 1] - current_history[i]
            for i in range(len(current_history) - 1)
        ]

        transformation.append(current_history[0])

    result: int = 0
    while transformation:
        result = transformation.pop() - result

    return result


def compute_new_value(file_name: str) -> int:
    result: int = 0

    with open(file_name) as file:
        for line in file:
            history: list[int] = [
                int(number)
                for number in line.strip("\n").split()
            ]
            result += get_previous_value(history)

    return result


def main(file_name: str = "./9/input.txt"):
    print(compute_new_value(file_name))


if __name__ == "__main__":
    main()
