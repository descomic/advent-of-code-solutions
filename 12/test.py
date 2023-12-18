from tokenize import group
from ddt import ddt, data, unpack
import main
import unittest


EXAMPLE: list[str] = [
    "???.### 1,1,3",
    ".??..??...?##. 1,1,3",
    "?#?#?#?#?#?#?#? 1,3,1,6",
    "????.#...#... 4,1,1",
    "????.######..#####. 1,6,5",
    "?###???????? 3,2,1",
]


@ddt
class Test(unittest.TestCase):

    def test_sum_of_arrangements(self):
        pass
        # self.assertEqual(525152, main.get_sum_of_arrangements(EXAMPLE))

    @unpack
    @data(
        (EXAMPLE[0], 1),
        (EXAMPLE[1], 16384),
        (EXAMPLE[2], 1),
        (EXAMPLE[3], 16),
        (EXAMPLE[4], 2500),
        (EXAMPLE[5], 506250),
    )
    def test_get_number_of_arrangements(self, line: str, expected: int):
        parse_record, parse_groups = line.split(" ")
        record: str = main.UNKNOWN.join([parse_record for _ in range(5)]) + "."
        groups: list[int] = [int(group)
                             for group in parse_groups.split(",")] * 5
        arrangements = main.get_arrangements(record,  tuple(groups))
        self.assertEqual(expected, arrangements)

    @unpack
    @data(
        ("#.#.###", [1, 1, 3], True),
        (".##.###", [1, 1, 3], False),

        (".#....#...###.", [1, 1, 3], True),

        (".#.###.#.######", [1, 3, 1, 6], True),
        (".#.###..#.######", [1, 3, 1, 6], True),

        ("####.#...#...", [4, 1, 1], True),
        ("###..#...#...", [4, 1, 1], False),

        ("#....######..#####.", [1, 6, 5], True),
        (".#...######..#####.", [1, 6, 5], True),
        ("..#..######..#####.", [1, 6, 5], True),
        ("...#.######..#####.", [1, 6, 5], True),

        (".###..##.#..", [3, 2, 1], True),
    )
    def test_matches_rule(self, record: str, rule: list[int], expected: bool):
        self.assertEqual(expected, main.matches_rule(record, rule))


if __name__ == '__main__':
    unittest.main()
