from ddt import ddt, data, unpack
import main
import unittest


@ddt
class Test(unittest.TestCase):

    @data(
        ([0, 3, 6, 9, 12, 15], 18),
        ([1, 3, 6, 10, 15, 21], 28),
        ([10, 13, 16, 21, 30, 45], 68),
    )
    @unpack
    def test_next_value(self, history: list[int], expected_next_value: int):
        self.assertEqual(expected_next_value, main.get_next_value(history))

    @data(
        ([0, 3, 6, 9, 12, 15], -3),
        ([1, 3, 6, 10, 15, 21], 0),
        ([10, 13, 16, 21, 30, 45], 5),
    )
    @unpack
    def test_previous_value(self, history: list[int], expected_next_value: int):
        self.assertEqual(expected_next_value, main.get_previous_value(history))

    def test_main(self):
        file_name: str = "./9/example.txt"
        self.assertEqual(2, main.compute_new_value(file_name))


if __name__ == "__main__":
    unittest.main()
