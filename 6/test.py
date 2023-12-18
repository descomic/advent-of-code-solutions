import main
import unittest


class Test(unittest.TestCase):
    def test(self):
        with open('./6/example.txt') as file:
            example: str = file.read()
            self.assertEqual(
                71503,
                main.get_number_of_ways(example)
            )


if __name__ == '__main__':
    unittest.main()
