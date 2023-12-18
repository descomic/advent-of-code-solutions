import main
import unittest

example_dish = [
    "O....#....",
    "O.OO#....#",
    ".....##...",
    "OO.#O....O",
    ".O.....O#.",
    "O.#..O.#.#",
    "..O..#O..O",
    ".......O..",
    "#....###..",
    "#OO..#....",
]

tilted_north = [
    "OOOO.#.O..",
    "OO..#....#",
    "OO..O##..O",
    "O..#.OO...",
    "........#.",
    "..#....#.#",
    "..O..#.O.O",
    "..O.......",
    "#....###..",
    "#....#....",
]

tilted_north_then_west = [
    "OOOO.#O...",
    "OO..#....#",
    "OOO..##O..",
    "O..#OO....",
    "........#.",
    "..#....#.#",
    "O....#OO..",
    "O.........",
    "#....###..",
    "#....#....",
]

tilted_north_then_west_then_south = [
    ".....#....",
    "....#.O..#",
    "O..O.##...",
    "O.O#......",
    "O.O....O#.",
    "O.#..O.#.#",
    "O....#....",
    "OO....OO..",
    "#O...###..",
    "#O..O#....",
]

tilted_north_then_west_then_south_then_east = [
    ".....#....",
    "....#...O#",
    "...OO##...",
    ".OO#......",
    ".....OOO#.",
    ".O#...O#.#",
    "....O#....",
    "......OOOO",
    "#...O###..",
    "#..OO#....",
]


class Test(unittest.TestCase):
    def test_total_load(self):
        self.assertEqual(64, main.compute_total_load("./14/example.txt"))

    def test_tilt_north(self):
        self.assertEqual(tilted_north, main.tilt_dish_north(example_dish))

    def test_tilt_dish_north_west(self):
        self.assertEqual(tilted_north_then_west,
                         main.tilt_dish_west(tilted_north))

    def test_tilt_north_west_south(self):
        self.assertEqual(
            tilted_north_then_west_then_south,
            main.tilt_dish_south(tilted_north_then_west),
        )

    def test_tilt_north_west_south_east(self):
        self.assertEqual(
            tilted_north_then_west_then_south_then_east,
            main.tilt_dish_east(tilted_north_then_west_then_south),
        )

    def test_tilt_dish_cycle(self):
        self.assertEqual(
            tilted_north_then_west_then_south_then_east,
            main.tilt_dish_cycle(example_dish),
        )

    def test_tilt(self):
        for i in range(len(example_dish[0])):
            self.assertEqual(
                "".join(line[i] for line in tilted_north),
                main.tilt("".join(line[i] for line in example_dish)),
            )


if __name__ == '__main__':
    unittest.main()
