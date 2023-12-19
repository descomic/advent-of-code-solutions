import unittest

import main


class MyTestCase(unittest.TestCase):
    def test_get_ultimate_rating(self):
        self.assertEqual(167409079868000, main.get_ultimate_rating("./example.txt"))


if __name__ == "__main__":
    unittest.main()
