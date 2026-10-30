---
name: gads-testing-qa
description: Derives test scenarios from acceptance criteria and risk, runs and automates tests, and reports QA evidence.
---

# GADS Testing and QA

## Purpose

Show with evidence whether a change meets its acceptance criteria, and that its tests can fail when the behavior breaks.

## Canonical policies

- `agents/qa-engineer.md` (procedure and boundaries of the QA role)
- `standard/WORKFLOW_AND_GATES.md` (quality gate, test selection, completion states)
- `standard/OPERATING_STANDARD.md` section 3 (test expectations)
- `templates/QA_REPORT.md` (report format)

## Inputs

- Acceptance criteria and changed behavior.
- Existing test commands and test environment.

## Outputs

- Scenario table: scenario, acceptance criterion, expected result, actual result, evidence.
- Exact commands run with outcomes (passed, failed, not run, blocked).
- QA conclusion: pass, pass with limitations, fail, or blocked.

## Constraints

- Edit tests and test data only. Report product defects instead of fixing them.
- Never weaken, skip, or delete a test to obtain a green result. A skipped test needs an explanation.
- A passing unit suite does not prove integration, security, or performance; say so in the report.
