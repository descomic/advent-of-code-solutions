import main
import unittest


EXAMPLE_FILE_NAME: str = "./18/example.txt"
EXAMPLE: list[tuple[str, int]] = [
    ('R', 6),
    ('D', 5),
    ('L', 2),
    ('D', 2),
    ('R', 2),
    ('D', 2),
    ('L', 5),
    ('U', 2),
    ('L', 1),
    ('U', 2),
    ('R', 2),
    ('U', 3),
    ('L', 2),
    ('U', 2),
]
EXAMPLE_TRENCH: list[str] = [
    "#######",
    "#.....#",
    "###...#",
    "..#...#",
    "..#...#",
    "###.###",
    "#...#..",
    "##..###",
    ".#....#",
    ".######",
]
EXAMPLE_EMPTY_POOL: list[str] = [
    "#######",
    "#######",
    "#######",
    "..#####",
    "..#####",
    "#######",
    "#####..",
    "#######",
    ".######",
    ".######",
]


class Test(unittest.TestCase):
    def test(self):
        self.assertEqual(
            952408144115,
            main.get_volume_of_pool(EXAMPLE_FILE_NAME)
        )


if __name__ == '__main__':
    unittest.main()
