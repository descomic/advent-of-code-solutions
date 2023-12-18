from hmac import new
import math
import sys
from unittest import result
from xmlrpc.client import Unmarshaller

SEED_TO_SOIL_MAP = "seed-to-soil map:"
SOIL_TO_FERTILIZER_MAP = "soil-to-fertilizer map:"
FERTILIZER_TO_WATER_MAP = "fertilizer-to-water map:"
WATER_TO_LIGHT_MAP = "water-to-light map:"
LIGHT_TO_TEMPERATURE_MAP = "light-to-temperature map:"
TEMPERATURE_TO_HUMIDITY_MAP = "temperature-to-humidity map:"
HUMIDITY_TO_LOCATION_MAP = "humidity-to-location map:"


def read_map(file: str, title: str) -> list[list[int]]:
    lines: list[str] = file.split("\n")

    start: int = lines.index(title)
    end: int = start

    for line in lines[start:]:
        if line == "":
            break
        end += 1

    map: list[list[int]] = [
        [int(value) for value in line.split()]
        for line in lines[start + 1:end]
    ]

    return map


def get_seeds(line: str) -> list[tuple[int, int]]:
    ranges: list[int] = [int(value)
                         for value in line.split(":")[1].strip().split()]
    return [(ranges[i], ranges[i + 1]) for i in range(0, len(ranges), 2)]


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []
    tmp: list[tuple[int, int]] = sorted(ranges, key=lambda x: x[0])

    current: tuple[int, int] = tmp[0]
    index: int = 1

    while index < len(tmp):
        if tmp[index][1] == 0:
            index += 1
        elif current[0] == tmp[index][0]:
            current = (current[0], max(current[1], tmp[index][1]))
            index += 1
        elif current[0] + current[1] == tmp[index][0]:
            current = (current[0], current[1] + tmp[index][1])
            index += 1
        elif current[0] + current[1] < tmp[index][0]:
            result.append(current)
            current = tmp[index]
            index += 1
        elif current[0] + current[1] <= tmp[index][0] + tmp[index][1]:
            new_length: int = current[1] + tmp[index][1] - \
                (tmp[index][0] + tmp[index][1] - (current[0] + current[1]))
            current = (current[0], new_length)
            index += 1
        else:
            index += 1
        if index == len(tmp):
            result.append(current)
    return result


def get_transformed_value(value: tuple[int, int], map: list[list[int]]) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []

    unmatched: list[tuple[int, int]] = [value]

    for rule in map:
        new_unmatched: list[tuple[int, int]] = []

        for unmatched_value in unmatched:
            start: int = unmatched_value[0]
            value_length: int = unmatched_value[1]
            end: int = start + value_length

            destination_range_start: int = rule[0]
            source_range_start: int = rule[1]
            rule_range_length: int = rule[2]
            source_range_end: int = source_range_start + rule_range_length

            if source_range_end <= start or end < source_range_start:
                new_unmatched.append(unmatched_value)
                continue
            elif start < source_range_start:
                if end < source_range_start:
                    continue
                elif end < source_range_end:
                    new_unmatched.append((start, source_range_start - start))
                    result.append((destination_range_start,
                                   end - source_range_start))
                else:
                    new_unmatched.append((start, source_range_start - start))
                    result.append((destination_range_start, rule_range_length))
                    new_unmatched.append(
                        (source_range_end, end - source_range_end))
            else:
                if end < source_range_end:
                    result.append((destination_range_start +
                                   (start - source_range_start), value_length))
                else:
                    result.append((destination_range_start +
                                   (start - source_range_start), source_range_end - start))
                    new_unmatched.append(
                        (source_range_end, end - source_range_end))

        unmatched = new_unmatched

    return result + unmatched


def get_value_from_map(map: list[list[int]], value: list[tuple[int, int]]) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []

    for set_of_values in value:
        result += get_transformed_value(set_of_values, map)

    return merge_ranges(result)


def get_minimum_location(file: str) -> int:
    lines: list[str] = file.split("\n")

    seeds: list[tuple[int, int]] = get_seeds(lines[0])

    seed_to_soil_map: list[list[int]] = read_map(file, SEED_TO_SOIL_MAP)
    soil_to_fertilizer_map: list[list[int]] = read_map(
        file, SOIL_TO_FERTILIZER_MAP)
    fertilizer_to_water_map: list[list[int]] = read_map(
        file, FERTILIZER_TO_WATER_MAP)
    water_to_light_map: list[list[int]] = read_map(file, WATER_TO_LIGHT_MAP)
    light_to_temperature_map: list[list[int]] = read_map(
        file, LIGHT_TO_TEMPERATURE_MAP)
    temperature_to_humidity_map: list[list[int]] = read_map(
        file, TEMPERATURE_TO_HUMIDITY_MAP)
    humidity_to_location_map: list[list[int]] = read_map(
        file, HUMIDITY_TO_LOCATION_MAP)

    soils: list[tuple[int, int]] = get_value_from_map(seed_to_soil_map, seeds)
    fertilizers: list[tuple[int, int]] = get_value_from_map(
        soil_to_fertilizer_map, soils)
    waters: list[tuple[int, int]] = get_value_from_map(
        fertilizer_to_water_map, fertilizers)
    lights: list[tuple[int, int]] = get_value_from_map(
        water_to_light_map, waters)
    temperatures: list[tuple[int, int]] = get_value_from_map(
        light_to_temperature_map, lights)
    humiditys: list[tuple[int, int]] = get_value_from_map(
        temperature_to_humidity_map, temperatures)
    locations: list[tuple[int, int]] = get_value_from_map(
        humidity_to_location_map, humiditys)
    return min([location[0] for location in locations])


def main(file_name: str = "./5/input.txt"):
    with open(file_name, "r") as file:
        print(get_minimum_location(file.read()))


if __name__ == '__main__':
    main()
