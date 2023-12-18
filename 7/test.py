from ddt import ddt, data, unpack
import main
import unittest

hands_and_bids: list[str] = [
    "32T3K 765",
    "T55J5 684",
    "KK677 28",
    "KTJJT 220",
    "QQQJA 483"
]


@ddt
class Test(unittest.TestCase):
    @data(

        ("AAAAA", "AAAAA", 0),
        ("AAAAA", "KKKKK", 1),
        ("KKKKK", "AAAAA", -1),
        ("AA8AA", "AA8AA", 0),
        ("AA8AA", "AA9AA", -1),
        ("AA9AA", "AA8AA", 1),

        ("22922", "23332", 1),
        ("23332", "22922", -1),
        ("23332", "23332", 0),
        ("23332", "23322", 1),
        ("23322", "23332", -1),

        ("TTT98", "TTT98", 0),
        ("TTT98", "TTT88", -1),
        ("TTT87", "TTT97", -1),

        ("22287", "23432", 1),
        ("23432", "22287", -1),
        ("23432", "23432", 0),
        ("23432", "23422", -1),
        ("23532", "23432", 1),

        ("A23A4", "A23A4", 0),
        ("A23A4", "A25A4", -1),
        ("A24A4", "A23A4", 1),

        ("23456", "23456", 0),
        ("23456", "34567", -1),
        ("34567", "23456", 1),

        ("J3456", "23456", 1),
        ("23456", "J3456", -1),

        ("32J45", "32345", -1),
        ("32345", "32J45", 1),

        ("22J45", "22245", -1),

        ("KTJJT 22", "QQQJA 48", 1),

        ('AJAAA 176', 'JJJJJ 194', 1),
        ('JJJJJ 194', 'AJAAA 176',  -1),
    )
    @unpack
    def test_comparator(self, left: str, right: str, expected: int):
        self.assertEqual(
            main.comparator(left, right),
            expected
        )

    def test_get_sorted_hands(self):
        self.assertEqual(
            [
                "32T3K 765",
                "KK677 28",
                "T55J5 684",
                "QQQJA 483",
                "KTJJT 220",
            ],
            main.get_sorted_hands(hands_and_bids)
        )

    def test(self):
        self.assertEqual(5905, main.get_total_winings(hands_and_bids))


if __name__ == '__main__':
    unittest.main()
