import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "release_gate.py"
spec = importlib.util.spec_from_file_location("release_gate", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

SHA = "3f786850e387550fdab836ed7e6dc881de23001b"


def report(**overrides):
    base = {"version": "1.0.0", "commit": SHA,
            "checks": [{"name": "tests", "status": "passed"}],
            "skipped_checks": [], "known_risks": [],
            "approvals": [{"action": "publish", "approver": "release owner"}],
            "rollback_plan": "revert"}
    base.update(overrides)
    return base


class ReleaseGateTests(unittest.TestCase):
    def test_valid_report(self):
        self.assertEqual(module.validate(report()), [])

    def test_missing_fields(self):
        errors = module.validate({})
        for field in module.REQUIRED_FIELDS:
            self.assertTrue(any(field in e for e in errors), field)

    def test_failed_check_blocks(self):
        errors = module.validate(report(checks=[{"name": "tests", "status": "failed"}]))
        self.assertTrue(any("status" in e for e in errors))

    def test_commit_must_be_full_sha(self):
        for commit in ["abc123", "REPLACE_WITH_FULL_COMMIT_SHA", "0" * 40, SHA.upper(), 42]:
            errors = module.validate(report(commit=commit))
            self.assertTrue(any("commit" in e for e in errors), commit)

    def test_empty_strings_rejected(self):
        self.assertTrue(module.validate(report(version=" ")))
        self.assertTrue(module.validate(report(rollback_plan="")))
        self.assertTrue(module.validate(report(known_risks=[""])))

    def test_skipped_checks_need_reason(self):
        errors = module.validate(report(skipped_checks=[{"name": "lint"}]))
        self.assertTrue(any("skipped_checks" in e for e in errors))

    def test_approvals_need_approver(self):
        errors = module.validate(report(approvals=[{"action": "publish", "approver": ""}]))
        self.assertTrue(any("approvals" in e for e in errors))

    def test_placeholders_rejected(self):
        errors = module.validate(report(approvals=[
            {"action": "publish", "approver": "REPLACE_WITH_ACCOUNTABLE_HUMAN"}]))
        self.assertIn("unfilled placeholder at report.approvals[0].approver", errors)

    def test_unfilled_example_fails(self):
        example = json.loads((ROOT / "scripts" / "example-release-report.json").read_text(encoding="utf-8"))
        errors = module.validate(example)
        self.assertTrue(errors)
        self.assertTrue(all("placeholder" in e or "commit" in e for e in errors), errors)

    def test_non_object_report(self):
        self.assertEqual(module.validate([]), ["report must be a JSON object"])


if __name__ == "__main__":
    unittest.main()
