#!/usr/bin/env python3
"""Validate release-report structure; does not authenticate evidence."""
import argparse
import json
import re
from pathlib import Path

REQUIRED_FIELDS = ["version", "commit", "checks", "skipped_checks", "known_risks",
                   "approvals", "rollback_plan"]
ACCEPTED = {"passed", "not_applicable"}
# Full SHA-1 or SHA-256 object name; abbreviated SHAs and placeholders are rejected.
COMMIT = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
PLACEHOLDER = "REPLACE_WITH"


def placeholders(value, path="report"):
    """Yield locations of unfilled template values."""
    if isinstance(value, str):
        if PLACEHOLDER in value:
            yield path
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from placeholders(item, f"{path}.{key}")
    elif isinstance(value, list):
        for i, item in enumerate(value):
            yield from placeholders(item, f"{path}[{i}]")


def nonempty_str(value):
    return isinstance(value, str) and bool(value.strip())


def check_records(report, field, keys, errors):
    """Validate a list of objects whose given keys are non-empty strings."""
    value = report[field]
    if not isinstance(value, list):
        errors.append(f"{field} must be a list")
        return
    for i, item in enumerate(value):
        if not isinstance(item, dict) or not all(nonempty_str(item.get(k)) for k in keys):
            errors.append(f"{field} {i} must contain non-empty {' and '.join(keys)}")


def validate(report):
    if not isinstance(report, dict):
        return ["report must be a JSON object"]
    errors = [f"missing required field: {f}" for f in REQUIRED_FIELDS if f not in report]
    errors += [f"unfilled placeholder at {loc}" for loc in placeholders(report)]
    if "version" in report and not nonempty_str(report["version"]):
        errors.append("version must be a non-empty string")
    if "commit" in report:
        commit = report["commit"]
        if not isinstance(commit, str) or not COMMIT.match(commit) or not commit.strip("0"):
            errors.append("commit must be a full lowercase commit SHA (40 or 64 hex characters)")
    if "checks" in report:
        if not isinstance(report["checks"], list) or not report["checks"]:
            errors.append("checks must be a non-empty list")
        else:
            for i, check in enumerate(report["checks"]):
                if not isinstance(check, dict) or not nonempty_str(check.get("name")) or "status" not in check:
                    errors.append(f"check {i} must contain name and status")
                elif check["status"] not in ACCEPTED:
                    errors.append(f"check {i} status must be passed or not_applicable")
    if "skipped_checks" in report:
        check_records(report, "skipped_checks", ["name", "reason"], errors)
    if "approvals" in report:
        check_records(report, "approvals", ["action", "approver"], errors)
    if "known_risks" in report:
        risks = report["known_risks"]
        if not isinstance(risks, list) or not all(nonempty_str(r) for r in risks):
            errors.append("known_risks must be a list of non-empty strings")
    if "rollback_plan" in report and not nonempty_str(report["rollback_plan"]):
        errors.append("rollback_plan must be a non-empty string")
    return errors


def main():
    p = argparse.ArgumentParser()
    p.add_argument("report")
    args = p.parse_args()
    try:
        report = json.loads(Path(args.report).read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: cannot read JSON report: {exc}")
        return 2
    errors = validate(report)
    if errors:
        print("RELEASE GATE: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("RELEASE GATE: STRUCTURE PASS (evidence not authenticated)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
