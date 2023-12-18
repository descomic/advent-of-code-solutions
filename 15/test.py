from ddt import ddt, data, unpack
import main
import unittest


@ddt
class Test(unittest.TestCase):
    def test_sum_of_hashes(self):
        self.assertEqual(main.get_focusing_power("./15/example.txt"), 145)

    @unpack
    @data(
        ("HASH", 52),
        ("rn=1", 30),
        ("cm-", 253),
        ("qp=3", 97),
        ("cm=2", 47),
        ("qp-", 14),
        ("pc=4", 180),
        ("ot=9", 9),
        ("ab=5", 197),
        ("pc-", 48),
        ("pc=6", 214),
        ("ot=7", 231),
    )
    def test_hash(self, input: str, expected: str):
        self.assertEqual(main.get_hash(input), expected)

    def test_hash_map(self):
        hash_map: main.HashMap = main.read_hash_map("./15/example.txt")
        self.assertEqual(hash_map.boxes[0].lenses, [("rn", 1), ("cm", 2)])
        self.assertEqual(hash_map.boxes[3].lenses, [
                         ("ot", 7), ("ab", 5), ("pc", 6)])
        self.assertEqual(hash_map.get_focusing_power(), 145)


if __name__ == '__main__':
    unittest.main()
