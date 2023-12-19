EXTREMELY_COOL_LOOKING: str = "x"
MUSICAL: str = "m"
AERODYNAMIC: str = "a"
SHINY: str = "s"

LOWER_THAN: str = "<"
GREATER_THAN: str = ">"


class SetOfParts:
    def __init__(
        self, interval: dict[str, tuple[int, int]], next_workflow: str
    ) -> None:
        self.interval: dict[str, tuple[int, int]] = interval
        self.next_workflow: str = next_workflow

    def copy(
        self, new_interval: dict[str, tuple[int, int]], new_destination: str
    ) -> "SetOfParts":
        new_parts: SetOfParts = SetOfParts(self.interval.copy(), new_destination)
        for key in new_interval:
            new_parts.interval[key] = new_interval[key]
        return new_parts

    def __eq__(self, other):
        if not isinstance(other, SetOfParts):
            return False
        return self.interval == other.interval

    def __hash__(self):
        return hash(tuple(sorted(self.interval.items())))


class Step:
    def applies(self, part: dict[str, int]) -> bool:
        raise NotImplementedError("Method Step.applies not implemented")

    def apply(self, part: dict[str, int]) -> str:
        raise NotImplementedError("Method Step.apply not implemented")

    def apply_to_interval(self, parts: SetOfParts) -> set[SetOfParts]:
        raise NotImplementedError("Method Step.apply_to_interval not implemented")


class ComparativeStep(Step):
    def __init__(
        self, rating_name: str, comparator: str, rating_value: int, destination: str
    ) -> None:
        self.rating_name: str = rating_name
        self.comparator: str = comparator
        self.rating_value: int = rating_value
        self.destination: str = destination

    def applies(self, part: dict[str, int]) -> bool:
        if self.comparator == LOWER_THAN:
            return part[self.rating_name] < self.rating_value
        elif self.comparator == GREATER_THAN:
            return part[self.rating_name] > self.rating_value
        else:
            raise ValueError(f"Invalid comparator {self.comparator}")

    def apply(self, part: dict[str, int]) -> str | None:
        if self.applies(part):
            return self.destination
        else:
            return None

    def apply_to_interval(self, parts: SetOfParts) -> set[SetOfParts]:
        if self.comparator == LOWER_THAN:
            if parts.interval[self.rating_name][1] < self.rating_value:
                return {SetOfParts(parts.interval, self.destination)}
            elif parts.interval[self.rating_name][0] < self.rating_value:
                part_1 = parts.copy(
                    {
                        self.rating_name: (
                            parts.interval[self.rating_name][0],
                            self.rating_value - 1,
                        )
                    },
                    self.destination,
                )
                part_2 = parts.copy(
                    {
                        self.rating_name: (
                            self.rating_value,
                            parts.interval[self.rating_name][1],
                        )
                    },
                    parts.next_workflow,
                )
                return {part_1, part_2}
        if self.comparator == GREATER_THAN:
            if parts.interval[self.rating_name][0] > self.rating_value:
                return {SetOfParts(parts.interval, self.destination)}
            elif parts.interval[self.rating_name][1] > self.rating_value:
                part_1 = parts.copy(
                    {
                        self.rating_name: (
                            parts.interval[self.rating_name][0],
                            self.rating_value,
                        )
                    },
                    parts.next_workflow,
                )
                part_2 = parts.copy(
                    {
                        self.rating_name: (
                            self.rating_value + 1,
                            parts.interval[self.rating_name][1],
                        )
                    },
                    self.destination,
                )
                return {part_1, part_2}
        return {parts}

    def __eq__(self, other):
        if not isinstance(other, ComparativeStep):
            return False
        return (
            self.rating_name == other.rating_name
            and self.comparator == other.comparator
            and self.rating_value == other.rating_value
            and self.destination == other.destination
        )

    def __str__(self):
        return f"{self.rating_name} {self.comparator} {self.rating_value} -> {self.destination}"


class LastStep(Step):
    def __init__(self, destination: str) -> None:
        self.destination: str = destination

    def applies(self, part: dict[str, int]) -> bool:
        return True

    def apply(self, part: dict[str, int]) -> str:
        return self.destination

    def apply_to_interval(self, parts: SetOfParts) -> set[SetOfParts]:
        new_parts: set[SetOfParts] = set()
        new_parts.add(SetOfParts(parts.interval, self.destination))
        return new_parts

    def __eq__(self, other):
        if not isinstance(other, LastStep):
            return False
        return self.destination == other.destination

    def __str__(self):
        return f"-> {self.destination}"


class Workflow:
    def __init__(self, name: str, steps: list[Step]) -> None:
        self.name: str = name
        self.steps: list[Step] = steps

    def apply(self, part: dict[str, int]) -> str:
        for step in self.steps:
            destination = step.apply(part)
            if destination:
                return destination
        raise ValueError("No destination found")

    def apply_to_interval(self, parts: SetOfParts) -> set[SetOfParts]:
        new_parts: set[SetOfParts] = {parts}
        for step in self.steps:
            applied_parts: set[SetOfParts] = set()
            for part in new_parts:
                if part.next_workflow != self.name:
                    applied_parts.add(part)
                else:
                    applied_parts.update(step.apply_to_interval(part))
            new_parts = applied_parts
        return new_parts

    def __eq__(self, other):
        if not isinstance(other, Workflow):
            return False
        return self.name == other.name and self.steps == other.steps

    def __str__(self):
        return f"{self.name}: {self.steps}"


def parse_step(value: str) -> Step:
    if ":" not in value:
        return LastStep(value)
    comparison, destination = value.split(":")
    if LOWER_THAN in value:
        rating_name, rating_value = comparison.split(LOWER_THAN)
        return ComparativeStep(rating_name, LOWER_THAN, int(rating_value), destination)
    elif GREATER_THAN in value:
        rating_name, rating_value = comparison.split(GREATER_THAN)
        return ComparativeStep(
            rating_name, GREATER_THAN, int(rating_value), destination
        )
    else:
        raise ValueError(f"Invalid comparison {comparison}")


def parse_workflow(line: str) -> Workflow:
    name, steps = line.split("{")
    steps = steps.strip("}")
    name = name.strip()
    steps = [parse_step(step) for step in steps.split(",")]
    return Workflow(name, steps)
