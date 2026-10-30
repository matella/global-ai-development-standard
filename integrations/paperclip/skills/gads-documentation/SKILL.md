---
name: gads-documentation
description: Keeps durable project documentation accurate, single-sourced and linked after behavior, interface or decision changes.
---

# GADS Documentation

## Purpose

Keep durable knowledge in version-controlled files, accurate, findable, and free of duplication.

## Canonical policies

- `agents/librarian.md` (procedure and boundaries of the documentation role)
- `standard/OPERATING_STANDARD.md` section 4 (documentation and knowledge)
- `templates/LESSON.md` and `templates/ADR.md` (durable knowledge formats)

## Inputs

- The change being documented, with its commit or diff.
- Affected documents (README, operations, ADRs, lessons).

## Outputs

- Updated documents, each stating which commit or decision it reflects.
- Superseded content marked as superseded rather than deleted silently.
- Lessons captured with `templates/LESSON.md` when the change exposed a reusable lesson.

## Constraints

- Update the single canonical location and link to it instead of duplicating text.
- Do not record unverified facts. Label assumptions.
- Do not place secrets, personal data, or real production identifiers in documentation.
- Documentation changes follow the same review and gate rules as code.
