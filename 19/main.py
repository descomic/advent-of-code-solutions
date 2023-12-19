from workflow import Workflow, parse_workflow, SetOfParts

REJECTED = "R"

ACCEPTED = "A"

IN = "in"

EXTREMELY_COOL_LOOKING: str = "x"
MUSICAL: str = "m"
AERODYNAMIC: str = "a"
SHINY: str = "s"

LOWER_THAN: str = "<"
GREATER_THAN: str = ">"


def parse_part(part: str) -> dict[str, int]:
    part = part.strip("{").strip("}")
    result: dict[str, int] = {}
    for part_string in part.split(","):
        rating_name, rating_value = part_string.split("=")
        result[rating_name] = int(rating_value)
    return result


def get_ultimate_rating(file_name: str) -> int:
    workflows: dict[str, Workflow] = {}
    with open(file_name) as file:
        for line in file.readlines():
            line = line.strip("\n")
            if not line or line.startswith("{"):
                break
            else:
                workflow: Workflow = parse_workflow(line)
                workflows[workflow.name] = workflow

    initial_parts: dict[str, tuple[int, int]] = {
        EXTREMELY_COOL_LOOKING: (1, 4000),
        MUSICAL: (1, 4000),
        AERODYNAMIC: (1, 4000),
        SHINY: (1, 4000),
    }
    parts: list[SetOfParts] = [
        SetOfParts(
            initial_parts,
            IN,
        )
    ]

    accepted_parts: list[dict[str, tuple[int, int]]] = list()
    while parts:
        new_parts: list[SetOfParts] = list()
        for set_of_parts in parts:
            workflow: Workflow = workflows[set_of_parts.next_workflow]
            applied: set[SetOfParts] = workflow.apply_to_interval(set_of_parts)
            for part in applied:
                if part.next_workflow == ACCEPTED:
                    accepted_parts.append(part.interval)
                elif part.next_workflow == REJECTED:
                    continue
                else:
                    new_parts.append(part)
        parts = new_parts

    result: int = 0
    for accepted in accepted_parts:
        combinations: int = 1
        for key in ["x", "m", "a", "s"]:
            n: int = accepted[key][1]
            j: int = accepted[key][0]
            combinations *= n - j + 1
        result += combinations
    return result


if __name__ == "__main__":
    print(get_ultimate_rating("./input.txt"))
