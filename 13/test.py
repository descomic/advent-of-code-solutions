from ddt import ddt, data, unpack
import main
import unittest

first_pattern = [
    "#.##..##.",
    "..#.##.#.",
    "##......#",
    "##......#",
    "..#.##.#.",
    "..##..##.",
    "#.#.##.#.",
]

second_pattern = [
    "#...##..#",
    "#....#..#",
    "..##..###",
    "#####.##.",
    "#####.##.",
    "..##..###",
    "#....#..#",
]

# geerate test cases similar to the ones above, but different
third_pattern = [
    "#.##..##.",
    "..#.##.#.",
    "##......#",
    "##......#",
    "..#.##.#.",
    "..##..##.",
    "#.#.##.#.",
]

fourth_pattern = [
    "..####...#.##..##",
    "####.#.......##..",
    "......##..#..##..",
    "#.....#####..#...",
    ".#.###...#.......",
    "..#.#..#.#...##..",
    "....##.##.#######",
    "###.##...#.#..#.#",
    ".##....###.##..##",
]


@ddt
class Test(unittest.TestCase):
    def test(self):
        self.assertEqual(400, main.compute_reflection("./13/example.txt"))

    @data(
        (300, first_pattern),
        (100, second_pattern),
        (300, third_pattern),
        (16, fourth_pattern)
    )
    @unpack
    def test_get_reflection(self, expeced_lines: int, pattern: list[str]):
        self.assertEqual(expeced_lines, main.get_reflection(pattern))


if __name__ == '__main__':
    unittest.main()
