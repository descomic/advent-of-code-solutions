import main
import unittest


class Test(unittest.TestCase):
    def test(self):
        self.assertEqual(2, main.get_steps("./8/example1.txt"))
        self.assertEqual(6, main.get_steps("./8/example2.txt"))
        self.assertEqual(6, main.get_steps("./8/example3.txt"))

    def test_parse_line(self):
        self.assertEqual(("A", ("B", "C")), main.parse_map_line("A = (B, C)"))
        self.assertEqual(("AAA", ("BBB", "CCC")),
                         main.parse_map_line("AAA = (BBB, CCC)"))
        self.assertEqual(("AAA", ("BBB", "CCC")),
                         main.parse_map_line("AAA = (BBB, CCC)\n"))


if __name__ == "__main__":
    unittest.main()
