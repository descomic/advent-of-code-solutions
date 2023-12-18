from main import sum_power_minimum
import unittest


class Test(unittest.TestCase):

    def test_example(self):
        with open("./2/test.txt", "r") as example:
            self.assertEqual(2286, sum_power_minimum(example))


if __name__ == '__main__':
    unittest.main()
