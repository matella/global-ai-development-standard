---
name: gads-architecture
description: Assesses design options for cross-cutting changes and drafts ADRs when GADS decision triggers apply. Read-only with respect to code.
---

# GADS Architecture

## Purpose

Choose the simplest design that meets the requirements and fits the existing system, and record durable decisions.

## Canonical policies

- `agents/architect.md` (procedure and boundaries of the architect role)
- `agents/skeptic.md` (counterexample and simplicity challenge, used before risky designs)
- `standard/DECISION_POLICY.md` (decision classes, ADR triggers, escalation format)
- `standard/OPERATING_STANDARD.md` section 2 (change design)
- `templates/ADR.md` (ADR format)

## Inputs

- Requirement or problem statement and quality attributes that matter.
- Current architecture documentation and affected components.

## Outputs

- At least two options, including the smallest incremental one, with trade-offs.
- Recommended option with rationale, rejected alternatives, migration path, and rollback.
- A draft ADR from `templates/ADR.md` when an ADR trigger applies.
- Open questions that require a human decision.

## Constraints

- Propose designs; do not implement them. Implementation belongs to the development skill.
- Cross-cutting decisions affecting security boundaries, data contracts, or deployment topology require escalation to an accountable human.
- Report facts, assumptions, and recommendations separately.
