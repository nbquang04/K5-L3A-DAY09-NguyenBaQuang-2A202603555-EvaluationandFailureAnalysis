"""Trace regression and FM-08 checks required by the Day 9 submission."""
import copy
import pytest

pytestmark = pytest.mark.student


def test_lab9_ticket_override_trace_regression():
    from lab9.trace_case import investigate
    bad = investigate("seeded_regression", "C-002", 11)["trial"]
    good = investigate("fixed", "C-002", 11)["trial"]
    assert bad["events"][1]["payload"]["lookup_order"]["order"]["delay_days"] == 2
    assert bad["events"][2]["kind"] == "model_override"
    assert bad["events"][2]["payload"]["delay_days"] == 5
    assert bad["snapshot"]["refund_vnd"] == 20000
    assert not bad["lab8_pass"]
    assert good["snapshot"]["refund_vnd"] == 0 and good["lab8_pass"]
    assert not any(e["kind"] == "model_override" for e in good["events"])


def test_lab9_reply_grader_catches_bug_that_lab8_accepts():
    from lab8.shapes import SHAPES
    from lab9.variant_agent import make_shape
    from lab9.trace_case import investigate
    from lab9.graders import ReplyAmountCorrect
    from pydantic_evals.evaluators import EvaluatorContext
    name = "test_reply_mismatch"
    SHAPES[name] = make_shape(name, {"no_override", "misreport"})
    try:
        for shape, expected in ((name, False), ("fixed", True)):
            case = investigate(shape, "C-008", 11)
            assert case["trial"]["lab8_pass"]
            ctx = EvaluatorContext(name="reply", inputs={}, metadata=None,
                expected_output=case["label"], output=case["trial"], duration=0,
                _span_tree=None, attributes={}, metrics={})
            assert ReplyAmountCorrect().evaluate(ctx).value is expected
    finally:
        SHAPES.pop(name)


def test_lab9_advanced_integrity_duplicate_and_green_evaluator_error():
    from lab9.gate import integrity_check
    base = {"manifest": {"items": 1, "seeds": [11, 22]},
            "rows": [{"item_id": "E-001", "seed": seed, "pass_rate": True, "slices": []} for seed in [11, 22]],
            "metrics": {"pass_rate": 1.0}, "evaluator_failures": []}
    spec = {"metrics": [{"id": "pass_rate", "kind": "capability", "threshold": {"min": .85}}]}
    duplicate = copy.deepcopy(base)
    duplicate["rows"][-1] = copy.deepcopy(duplicate["rows"][0])
    assert integrity_check(duplicate, base, spec)
    error = copy.deepcopy(base)
    error["evaluator_failures"] = ["grader crashed on an otherwise green run"]
    assert integrity_check(error, base, spec)
