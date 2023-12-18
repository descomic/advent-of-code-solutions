import functools
import re
from tokenize import group


UNKNOWN: str = "?"
OPERATIONAL: str = "."
DAMAGED: str = "#"


def matches_rule(record: str, rule: list[int]) -> bool:
    if record.count(DAMAGED) != sum(rule):
        return False

    rule_copy: list[int] = rule.copy()

    current_group: int = 0
    for character in record:
        if character == DAMAGED:
            current_group += 1
        elif character == OPERATIONAL and current_group > 0:
            if rule_copy:
                if current_group != rule_copy.pop(0):
                    return False
            else:
                return False
            current_group = 0

    if len(rule_copy) == 0 and current_group == 0:
        return True

    if len(rule_copy) == 1 and current_group == rule_copy[0]:
        return True

    return False


def process_damaged(record, groups, next_group) -> int:
    this_group: str = record[:next_group].replace(UNKNOWN, DAMAGED)

    if this_group != next_group * DAMAGED:
        return 0

    if len(record) == next_group:
        if len(groups) == 1:
            return 1
        else:
            return 0

    if record[next_group] in "?.":
        return get_arrangements(record[next_group+1:], groups[1:])

    return 0


def process_operational(record, groups) -> int:
    return get_arrangements(record[1:], groups)


@functools.cache
def get_arrangements(record: str, groups: tuple) -> int:
    if not groups:
        if DAMAGED not in record:
            return 1
        else:
            return 0

    if not record:
        return 0

    result: int = 0
    character: str = record[0]
    next_group: int = groups[0]

    if character == DAMAGED:
        result = process_damaged(record, groups, next_group)

    elif character == OPERATIONAL:
        result = process_operational(record, groups)

    elif character == UNKNOWN:
        result = process_damaged(record, groups, next_group) +\
            process_operational(record, groups)

    else:
        raise RuntimeError("Invalid character")

    return result


def get_sum_of_arrangements(lines: list[str]) -> int:
    result: int = 0

    for line in lines:
        parse_record, parse_groups = line.split(" ")

        record: str = UNKNOWN.join([parse_record for _ in range(5)])
        groups: list[int] = [int(group)
                             for group in parse_groups.split(",")] * 5
        result += get_arrangements(record, tuple(groups))

    return result


def main(file_name: str = "./12/input.txt") -> None:
    lines: list[str] = []
    with open(file_name, "r") as file:
        lines = [line.strip('\n') for line in file.readlines()]
    print(get_sum_of_arrangements(lines))


if __name__ == "__main__":
    main()
