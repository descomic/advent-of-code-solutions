import main
import unittest


universe: list[list[str]] = [
    list("...#......"),
    list(".......#.."),
    list("#........."),
    list(".........."),
    list("......#..."),
    list(".#........"),
    list(".........#"),
    list(".........."),
    list(".......#.."),
    list("#...#.....")
]


class Test(unittest.TestCase):

    def test_expand_universe(self):
        expected_empty_rows: list[int] = [3, 7]
        expected_empty_columns: list[int] = [2, 5, 8]
        empty_rows, empty_colums = main.expand_universe(universe)
        self.assertEqual(expected_empty_rows, empty_rows)
        self.assertEqual(expected_empty_columns, empty_colums)

    def test_sum_of_shortest_paths(self):
        self.assertEqual(374, main.sum_of_shortest_paths(universe, 2))
        self.assertEqual(1030, main.sum_of_shortest_paths(universe, 10))
        self.assertEqual(8410, main.sum_of_shortest_paths(universe, 100))

    def test_parse_universe(self):
        expected_universe: list[list[str]] = [
            list("...#......"),
            list(".......#.."),
            list("#........."),
            list(".........."),
            list("......#..."),
            list(".#........"),
            list(".........#"),
            list(".........."),
            list(".......#.."),
            list("#...#.....")
        ]
        self.assertEqual(expected_universe, main.parse_universe(
            '''...#......\n\
            .......#..\n\
            #.........\n\
            ..........\n\
            ......#...\n\
            .#........\n\
            .........#\n\
            ..........\n\
            .......#..\n\
            #...#.....'''))


if __name__ == '__main__':
    unittest.main()
