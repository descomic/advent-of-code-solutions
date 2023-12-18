RIGHT: str = 'R'
LEFT: str = 'L'
UP: str = 'U'
DOWN: str = 'D'

DUG: str = '#'
LEVEL: str = '.'

INT_TO_DIRECTION: dict[int, str] = {
    0: RIGHT,
    1: DOWN,
    2: LEFT,
    3: UP,
}


class Vertex():
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y


def compute_vertex(instructions: list[tuple[str, int]]) -> list[Vertex]:
    vertices: list[Vertex] = []
    current: Vertex = Vertex(0, 0)
    vertices.append(current)

    for instruction in instructions:
        direction: str = instruction[0]
        distance: int = instruction[1]

        if direction == RIGHT:
            current = Vertex(current.x + distance, current.y)
        elif direction == LEFT:
            current = Vertex(current.x - distance, current.y)
        elif direction == UP:
            current = Vertex(current.x, current.y + distance)
        elif direction == DOWN:
            current = Vertex(current.x, current.y - distance)
        else:
            raise Exception('Unknown direction')
        vertices.append(current)

    return vertices


def get_polygon_area(vertices: list[Vertex]) -> int:
    inside: int = 0
    outside: int = 0
    for i in range(len(vertices)):
        j = (i + 1) % len(vertices)
        inside += (vertices[i].x * vertices[j].y -
                   vertices[j].x * vertices[i].y)
        outside += abs(vertices[i].y - vertices[j].y +
                       (vertices[i].x - vertices[j].x))

    inside = abs(inside) // 2
    area: int = inside + (outside // 2) + 1
    return area


def get_volume_of_pool(file_name: str) -> int:
    instructions: list[tuple[str, int]] = []
    with open(file_name, 'r') as file:
        for line in file.read().splitlines():
            direction, distance, color = line.split()
            instructions.append(
                (INT_TO_DIRECTION[int(color[7])], int(color[2:7], base=16)))
    vertices: list[Vertex] = compute_vertex(instructions)
    return get_polygon_area(vertices)


if __name__ == '__main__':
    print(get_volume_of_pool('./18/input.txt'))
