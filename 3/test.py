from main import get_sum_of_part_numbers
import unittest


INPUT: str = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


class Test(unittest.TestCase):
    def test(self):
        self.assertEqual(467835, get_sum_of_part_numbers(INPUT.split("\n")))
        self.assertEqual(0, get_sum_of_part_numbers(
            ["....554", ".......", ".......", "......."]))


if __name__ == "__main__":
    unittest.main()
