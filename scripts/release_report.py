#!/usr/bin/env python3
"""Run the release checks and write a release report from their real results."""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
CHECKS = [
    ("unit-tests", [PY, "-m", "unittest", "discover", "-s", "tests"]),
    ("manifest-verification", [PY, "scripts/verify_manifest.py"]),
    ("repository-audit", [PY, "scripts/repo_audit.py", "."]),
    ("python-lint", ["ruff", "check", "."]),
    ("markdown-lint", ["markdownlint-cli2", "**/*.md"]),
]
PLACEHOLDER_APPROVER = "REPLACE_WITH_ACCOUNTABLE_HUMAN"


def run_checks(only=None):
    checks, skipped = [], []
    for name, command in CHECKS:
        if only and name not in only:
            continue
        if shutil.which(command[0]) is None:
            skipped.append({"name": name, "reason": f"{command[0]} is not installed"})
            continue
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        status = "passed" if result.returncode == 0 else "failed"
        shown = command[1:] if command[0] == PY else command
        checks.append({"name": name, "status": status, "command": " ".join(shown)})
        print(f"[{status.upper()}] {name}", file=sys.stderr)
    return checks, skipped


def git_head():
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                          text=True, check=True).stdout.strip()


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", required=True)
    p.add_argument("--commit", help="defaults to git rev-parse HEAD")
    p.add_argument("--approver",
                   help="accountable human; left as a placeholder when omitted, so the gate fails")
    p.add_argument("--approval-action", default="Publish the release")
    p.add_argument("--risk", action="append",
                   default=["The release gate checks structure; it does not authenticate evidence."])
    p.add_argument("--only", action="append", choices=[name for name, _ in CHECKS],
                   help="run only the named checks (repeatable)")
    p.add_argument("--rollback-plan", default="Delete the GitHub release, then publish a corrected version; "
                                              "consumers stay pinned to the previous tag.")
    args = p.parse_args(argv)
    checks, skipped = run_checks(args.only)
    report = {
        "version": (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        "commit": args.commit or git_head(),
        "checks": checks,
        "skipped_checks": skipped,
        "known_risks": args.risk,
        "approvals": [{"action": args.approval_action, "approver": args.approver or PLACEHOLDER_APPROVER}],
        "rollback_plan": args.rollback_plan,
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
