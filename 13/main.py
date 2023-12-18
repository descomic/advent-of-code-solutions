def match(row: list[str], other: list[str], smudges: list[tuple[int, int]]) -> bool:
    for i in range(len(row)):
        for j in range(len(row[0])):
            if row[i][j] != other[i][j]:
                smudges.append((i, j))
    return True


def get_reflection(pattern: list[str]) -> int:
    smudges: list[tuple[int, int]] = []
    for i in range(1, len(pattern)):
        if match(list(pattern[i]), list(pattern[i - 1]), smudges) and len(smudges) <= 1:
            j = 1
            while i - 1 - j >= 0 and i + j < len(pattern):
                match(list(pattern[i - 1 - j]), list(pattern[i + j]), smudges)
                j += 1

            if len(smudges) == 1:
                return i * 100
        smudges = []

    for i in range(1, len(pattern[0])):
        if match([line[i] for line in pattern], [line[i - 1] for line in pattern], smudges) and len(smudges) <= 1:
            j = 1
            while i - 1 - j >= 0 and i + j < len(pattern[0]):
                match([line[i - 1 - j] for line in pattern], [line[i + j]
                      for line in pattern], smudges)
                j += 1

            if len(smudges) == 1:
                return i
        smudges = []

    raise RuntimeError("No reflection found")


def compute_reflection(file_name: str) -> int:
    result: int = 0
    with open(file_name, "r") as file:
        for pattern in file.read().split("\n\n"):
            result += get_reflection(pattern.split("\n"))
    return result


if __name__ == "__main__":
    print(compute_reflection("./13/input.txt"))
