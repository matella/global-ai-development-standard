---
name: gads-release-management
description: Prepares a release from evidence: version consistency, release report, release gate, rollback plan. Never tags or publishes without approval.
---

# GADS Release Management

## Purpose

Prepare a release that an accountable human can approve from evidence alone.

## Canonical policies

- `agents/release-engineer.md` (procedure and boundaries of the release role)
- `standard/WORKFLOW_AND_GATES.md` (release gate and release evidence)
- `standard/SECURITY_AND_AUTONOMY.md` section 3 (publishing releases requires explicit approval)
- `docs/RELEASE.md` (release procedure of this repository)
- `scripts/release_gate.py` and `scripts/release_report.py` (structure check and report generation)

## Inputs

- Target version and the commit to release.
- `VERSION`, `CHANGELOG.md`, and `MANIFEST.json` state.

## Outputs

- Consistent `VERSION`, changelog section, and manifest.
- Release report produced from real check results, passing `release_gate.py`.
- Release notes, rollback plan, and the exact publish command for the human to approve.

## Constraints

- Never create tags, publish, or deploy without explicit approval naming the action and scope.
- The release gate checks structure only; it does not authenticate evidence. Say so in the report.
- Do not overwrite an existing tag or release. If a tag already exists, report it and stop.
- Do not alter approvals or placeholder values to pass the gate.
