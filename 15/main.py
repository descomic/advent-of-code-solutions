EQUAL: str = "="
REMOVE: str = "-"


def get_hash(input: str) -> int:
    current_value: int = 0
    for character in input:
        current_value += ord(character)
        current_value = current_value * 17
        current_value = current_value % 256
    return current_value


class Box:
    def __init__(self, box_number: int):
        self.box_number: int = box_number
        self.lenses: list[tuple[str, int]] = []

    def add_lens(self, label: str, focal_length: int):
        for i in range(len(self.lenses)):
            if self.lenses[i][0] == label:
                self.lenses[i] = (label, focal_length)
                return
        self.lenses.append((label, focal_length))

    def remove_lens(self, label: str):
        for i in range(len(self.lenses)):
            if self.lenses[i][0] == label:
                self.lenses.pop(i)
                return


class HashMap:
    def __init__(self):
        self.boxes: list[Box] = [Box(i) for i in range(256)]

    def add_lens(self, label: str, focal_length: int):
        box_number: int = get_hash(label)
        box: Box = self.boxes[box_number]
        box.add_lens(label, focal_length)

    def remove_lens(self, label: str):
        box_number: int = get_hash(label)
        box: Box = self.boxes[box_number]
        box.remove_lens(label)

    def get_focusing_power(self) -> int:
        result: int = 0

        for box in self.boxes:
            for i, lens in enumerate(box.lenses):
                result += (box.box_number + 1) * (i + 1) * lens[1]
        return result


def read_hash_map(file_name):
    hash_map: HashMap = HashMap()
    with open(file_name) as file:
        strings: list[str] = file.read().split(",")

        for instruction in strings:
            if EQUAL in instruction:
                label, focal_length = instruction.split(EQUAL)
                hash_map.add_lens(label, int(focal_length))
            elif REMOVE in instruction:
                label = instruction[:-1]
                hash_map.remove_lens(label)
            else:
                raise ValueError(f"Unknown instruction: {instruction}")
    return hash_map


def get_focusing_power(file_name: str) -> int:
    hash_map: HashMap = read_hash_map(file_name)
    return hash_map.get_focusing_power()


if __name__ == '__main__':
    print(get_focusing_power("./15/input.txt"))
