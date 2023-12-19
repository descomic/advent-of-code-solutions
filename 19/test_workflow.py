import unittest

from ddt import ddt, unpack, data

from workflow import (
    parse_step,
    ComparativeStep,
    LastStep,
    Workflow,
    parse_workflow,
    SetOfParts,
)


@ddt
class TestWorkflow(unittest.TestCase):
    @data(
        (
            "px{a<2006:qkq,m>2090:A,rfg}",
            Workflow(
                "px",
                [
                    ComparativeStep("a", "<", 2006, "qkq"),
                    ComparativeStep("m", ">", 2090, "A"),
                    LastStep("rfg"),
                ],
            ),
        ),
        (
            "pv{a>1716:R,A}",
            Workflow("pv", [ComparativeStep("a", ">", 1716, "R"), LastStep("A")]),
        ),
        (
            "lnx{m>1548:A,A}",
            Workflow("lnx", [ComparativeStep("m", ">", 1548, "A"), LastStep("A")]),
        ),
        (
            "qs{m<1548:R,A}",
            Workflow("qs", [ComparativeStep("m", "<", 1548, "R"), LastStep("A")]),
        ),
    )
    @unpack
    def test_parse_workflow(self, line: str, workflow: Workflow):
        self.assertEqual(workflow, parse_workflow(line))

    @data(
        ("a<2006:qkq", ComparativeStep("a", "<", 2006, "qkq")),
        ("m>2090:A", ComparativeStep("m", ">", 2090, "A")),
        ("rfg", LastStep("rfg")),
    )
    @unpack
    def test_parse_step(self, value: str, expected_step):
        self.assertEqual(expected_step, parse_step(value))

    def test_step_applies(self):
        step = ComparativeStep("a", "<", 2006, "qkq")
        self.assertTrue(step.applies({"a": 2005}))
        self.assertFalse(step.applies({"a": 2006}))
        self.assertFalse(step.applies({"a": 2007}))

    def test_step_apply(self):
        step = ComparativeStep("a", "<", 2006, "qkq")
        self.assertEqual("qkq", step.apply({"a": 2005}))

    def test_workflow_apply(self):
        workflow = Workflow(
            "px",
            [
                ComparativeStep("a", "<", 2006, "qkq"),
                ComparativeStep("m", ">", 2090, "A"),
                LastStep("rfg"),
            ],
        )
        self.assertEqual("qkq", workflow.apply({"a": 2005, "m": 2091}))
        self.assertEqual("A", workflow.apply({"a": 2007, "m": 2091}))
        self.assertEqual("rfg", workflow.apply({"a": 2007, "m": 2090}))

    @data(
        (
            SetOfParts(
                {"a": (1, 4000), "m": (1, 4000), "r": (1, 4000), "s": (1, 4000)}, "in"
            ),
            {
                SetOfParts(
                    {"a": (1, 2005), "m": (1, 4000), "r": (1, 4000), "s": (1, 4000)},
                    "qkq",
                ),
                SetOfParts(
                    {
                        "a": (2006, 4000),
                        "m": (2091, 4000),
                        "r": (1, 4000),
                        "s": (1, 4000),
                    },
                    "A",
                ),
                SetOfParts(
                    {
                        "a": (2006, 4000),
                        "m": (1, 2090),
                        "r": (1, 4000),
                        "s": (1, 4000),
                    },
                    "rfg",
                ),
            },
        ),
    )
    @unpack
    def test_workflow_apply_to_interval(self, parts: SetOfParts, expected: SetOfParts):
        workflow = Workflow(
            "in",
            [
                ComparativeStep("a", "<", 2006, "qkq"),
                ComparativeStep("m", ">", 2090, "A"),
                LastStep("rfg"),
            ],
        )
        applied = workflow.apply_to_interval(parts)
        self.assertEqual(expected, applied)


if __name__ == "__main__":
    unittest.main()
