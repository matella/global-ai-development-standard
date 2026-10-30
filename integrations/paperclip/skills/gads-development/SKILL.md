---
name: gads-development
description: Implements one accepted, scoped change with tests, following GADS change-design and code-quality rules.
---

# GADS Development

## Purpose

Deliver the smallest coherent change that satisfies an accepted task, with tests and documentation updates where behavior changes.

## Canonical policies

- `agents/developer.md` (procedure and boundaries of the developer role)
- `standard/OPERATING_STANDARD.md` sections 2 to 4 (change design, code quality, documentation)
- `standard/WORKFLOW_AND_GATES.md` (implement, verify, test selection)
- `standard/SECURITY_AND_AUTONOMY.md` (R2 changes need explanation; dependency controls in section 5)

## Inputs

- Accepted task with acceptance criteria.
- Relevant code and `gads/PROJECT.md` or the project's equivalent rules.

## Outputs

- Files changed and the reason for each.
- Exact commands run, each marked passed, failed, not run, or blocked.
- Remaining risks and follow-ups.

## Constraints

- Write or update a failing test first when the change is testable; do not weaken existing tests.
- Do not add dependencies, change CI, or change authentication or configuration without stating why and seeking approval where project policy requires it.
- Do not commit or push unless the task authorizes it. Do not rewrite history.
- Keep the diff scoped; inspect the full diff before reporting.
