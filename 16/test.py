import main
import unittest

EXAMPLE: list[str] = [
    ".|...\\....",
    "|.-.\\.....",
    ".....|-...",
    "........|.",
    "..........",
    ".........\\",
    "..../.\\\\..",
    ".-.-/..|..",
    ".|....-|.\\",
    "..//.|....",
]


class Test(unittest.TestCase):
    def test_number_of_energized_tiles(self):
        self.assertEqual(
            51, main.get_best_number_of_energized_tiles("./16/example.txt")
        )

    def test_get_beam_through(self):
        grid: list[str] = EXAMPLE.copy()
        result: int = main.pass_beam_through(grid, 0, 0, 0, 1)
        self.assertEqual(46, result)


if __name__ == "__main__":
    unittest.main()
