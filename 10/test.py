from ddt import ddt, data, unpack
import main
import unittest


@ddt
class Test(unittest.TestCase):

    @data(
        (4, "./10/example1.txt"),
        (8, "./10/example2.txt"),
    )
    @unpack
    def test_max_steps(self, expected: int, file_name: str):
        self.assertEqual(expected, main.get_max_step(file_name))

    @data(
        (0, "./10/example1.txt"),
        (0, "./10/example2.txt"),
        (4, "./10/example3.txt"),
        (4, "./10/example4.txt"),
        (8, "./10/example5.txt"),
        (10, "./10/example6.txt"),
    )
    @unpack
    def test_number_inside(self, expected: int, file_name: str):
        self.assertEqual(expected, main.get_number_inside(file_name))


if __name__ == "__main__":
    unittest.main()
