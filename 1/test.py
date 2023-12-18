from main import convert_spelled_out_digits_to_numbers, get_sum_of_calibration_values
import unittest


class Test(unittest.TestCase):

    def test_get_sum_of_calibration_values(self):
        lines: list[str] = ['1abc2',
                            'pqr3stu8vwx',
                            'a1b2c3d4e5f',
                            'treb7uchet',]
        expected_result: int = 142

        self.assertEqual(get_sum_of_calibration_values(lines), expected_result)

    def test_convert_spelled_out_digits_to_numbers(self):
        self.assertEqual(
            convert_spelled_out_digits_to_numbers('two1nine'),
            '219')
        self.assertEqual(
            convert_spelled_out_digits_to_numbers('eightwothree'),
            '8wo3')

    def test_get_sum_of_calibration_values_with_spelled_out_digigts(self):
        lines: list[str] = ['two1nine',
                            'eightwothree',
                            'abcone2threexyz',
                            'xtwone3four',
                            '4nineeightseven2',
                            'zoneight234',
                            '7pqrstsixteen',
                            ]
        expected_result: int = 281

        self.assertEqual(get_sum_of_calibration_values(lines), expected_result)


if __name__ == '__main__':
    unittest.main()
