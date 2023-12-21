import unittest

from ddt import ddt, unpack, data

from modules import (
    BroadcastModule,
    parse_module,
    parse_modules,
    FlipFlopModule,
    ConjunctionModule,
    ButtonModule,
    Module,
)

FIRST_EXAMPLE: list[str] = [
    "broadcaster -> a, b, c",
    "%a -> b",
    "%b -> c",
    "%c -> inv",
    "&inv -> a",
]


@ddt
class Test(unittest.TestCase):
    @unpack
    @data(
        (FIRST_EXAMPLE[0], BroadcastModule, "broadcaster", {"a", "b", "c"}),
        (FIRST_EXAMPLE[1], FlipFlopModule, "a", {"b"}),
        (FIRST_EXAMPLE[2], FlipFlopModule, "b", {"c"}),
        (FIRST_EXAMPLE[3], FlipFlopModule, "c", {"inv"}),
        (FIRST_EXAMPLE[4], ConjunctionModule, "inv", {"a"}),
    )
    def test_parse_module(
        self,
        line: str,
        expected_type: type,
        expected_name: str,
        expected_destination_modules: set[str],
    ):
        module, name_of_destinations = parse_module(line)

        self.assertIsInstance(module, expected_type)
        self.assertEqual(expected_name, module.name)
        self.assertEqual(len(expected_destination_modules), len(name_of_destinations))
        for nodule_name in expected_destination_modules:
            self.assertIn(nodule_name, name_of_destinations)

    def test_parse_modules(self):
        button: ButtonModule = parse_modules(FIRST_EXAMPLE)

        self.assertIsInstance(button, ButtonModule)
        self.assertEqual("button", button.name)
        self.assertEqual(1, len(button.destination_modules))
        self.assertIsInstance(button.destination_modules[0], BroadcastModule)

        broadcast_module: Module = button.destination_modules[0]

        self.assertEqual("broadcaster", broadcast_module.name)
        self.assertEqual(3, len(broadcast_module.destination_modules))

        a_module: Module = broadcast_module.destination_modules[0]
        b_module: Module = broadcast_module.destination_modules[1]
        c_module: Module = broadcast_module.destination_modules[2]

        self.assertIsInstance(a_module, FlipFlopModule)
        self.assertIsInstance(b_module, FlipFlopModule)
        self.assertIsInstance(c_module, FlipFlopModule)

        self.assertEqual(1, len(a_module.destination_modules))
        self.assertEqual("b", a_module.destination_modules[0].name)
        self.assertEqual(1, len(b_module.destination_modules))
        self.assertEqual("c", b_module.destination_modules[0].name)
        self.assertEqual(1, len(c_module.destination_modules))
        self.assertEqual("inv", c_module.destination_modules[0].name)

        inv: Module = c_module.destination_modules[0]
        self.assertIsInstance(inv, ConjunctionModule)
        self.assertEqual(1, len(inv.destination_modules))
        self.assertEqual("a", inv.destination_modules[0].name)

    def test_flip_flop_signal(self):
        flip_flop: FlipFlopModule = FlipFlopModule("savate")

        self.assertEqual(None, flip_flop.process_signal(1))
        self.assertEqual(1, flip_flop.process_signal(0))
        self.assertEqual(None, flip_flop.process_signal(1))
        self.assertEqual(0, flip_flop.process_signal(0))

    def test_conjunction_module(self):
        conjunction: ConjunctionModule = ConjunctionModule("conjunction")

        caller_1: str = "caller_1"
        caller_2: str = "caller_2"
        conjunction.add_caller(caller_1)
        conjunction.add_caller(caller_2)

        self.assertEqual(1, conjunction.process_signal(0, caller_1))
        self.assertEqual(1, conjunction.process_signal(0, caller_2))
        self.assertEqual(1, conjunction.process_signal(1, caller_1))
        self.assertEqual(0, conjunction.process_signal(1, caller_2))
        self.assertEqual(0, conjunction.process_signal(1, caller_1))
        self.assertEqual(1, conjunction.process_signal(0, caller_1))

    def test_broadcast_module(self):
        broadcast: BroadcastModule = BroadcastModule("broadcast")
        self.assertEqual(0, broadcast.process_signal(0))
        self.assertEqual(1, broadcast.process_signal(1))


if __name__ == "__main__":
    print(unittest.main())
