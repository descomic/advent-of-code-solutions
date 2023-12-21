from unittest import TestCase

import main
from modules import ButtonModule, parse_modules

FIRST_EXAMPLE: list[str] = [
    "broadcaster -> a, b, c",
    "%a -> b",
    "%b -> c",
    "%c -> inv",
    "&inv -> a",
]

SECOND_EXAMPLE: list[str] = [
    "broadcaster -> a",
    "%a -> inv, con",
    "&inv -> b",
    "%b -> con",
    "&con -> output",
]


class Test(TestCase):
    def test_compute_total_number_low_times_high_pulses_easy(self):
        self.assertEqual(
            32000000,
            main.compute_total_number_low_times_high_pulses("first_example.txt"),
        )

    def test_compute_total_number_low_times_high_pulses_hard(self):
        self.assertEqual(
            11687500,
            main.compute_total_number_low_times_high_pulses("second_example.txt"),
        )

    def test_press_button_first_example(self):
        button: ButtonModule = parse_modules(FIRST_EXAMPLE)
        expected_result: list[str] = [
            "button -low-> broadcaster",
            "broadcaster -low-> a",
            "broadcaster -low-> b",
            "broadcaster -low-> c",
            "a -high-> b",
            "b -high-> c",
            "c -high-> inv",
            "inv -low-> a",
            "a -low-> b",
            "b -low-> c",
            "c -low-> inv",
            "inv -high-> a",
        ]
        self.assertEqual(expected_result, main.press_button(button))

    def test_press_button_second_example(self):
        button: ButtonModule = parse_modules(SECOND_EXAMPLE)
        first_expected_result: list[str] = [
            "button -low-> broadcaster",
            "broadcaster -low-> a",
            "a -high-> inv",
            "a -high-> con",
            "inv -low-> b",
            "con -high-> output",
            "b -high-> con",
            "con -low-> output",
        ]
        self.assertEqual(first_expected_result, main.press_button(button))
        second_expected_result: list[str] = [
            "button -low-> broadcaster",
            "broadcaster -low-> a",
            "a -low-> inv",
            "a -low-> con",
            "inv -high-> b",
            "con -high-> output",
        ]
        self.assertEqual(second_expected_result, main.press_button(button))
        third_expected_result: list[str] = [
            "button -low-> broadcaster",
            "broadcaster -low-> a",
            "a -high-> inv",
            "a -high-> con",
            "inv -low-> b",
            "con -low-> output",
            "b -low-> con",
            "con -high-> output",
        ]
        self.assertEqual(third_expected_result, main.press_button(button))
        last_expected_result: list[str] = [
            "button -low-> broadcaster",
            "broadcaster -low-> a",
            "a -low-> inv",
            "a -low-> con",
            "inv -high-> b",
            "con -high-> output",
        ]
        self.assertEqual(last_expected_result, main.press_button(button))
        self.assertEqual(first_expected_result, main.press_button(button))
