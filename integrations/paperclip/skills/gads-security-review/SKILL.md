---
name: gads-security-review
description: Reviews a change for security issues including secrets, permissions, injection paths, dependency risk and autonomy-boundary violations. Read-only.
---

# GADS Security Review

## Purpose

Identify security defects and policy violations in a change before merge, and escalate what needs a human decision.

## Canonical policies

- `standard/SECURITY_AND_AUTONOMY.md` (threat model, risk tiers, approvals, secrets, supply chain, prompt injection)
- `agents/reviewer.md` (the review procedure whose security checks this skill extends)
- `standard/DECISION_POLICY.md` (security decisions escalate to the accountable human)

## Inputs

- The diff or repository state under review.
- Dependency changes, configuration changes, and any new external integrations.

## Outputs

- Findings by severity with location, exploit or failure scenario, and recommended mitigation.
- Explicit list of secrets or personal data found, redacted.
- Escalations: security, privacy, or permission decisions with options and recommendation.

## Constraints

- Do not exercise exploits against systems you are not authorized to test. Local, reproducible checks only.
- Do not print secret values in findings; reference the location only.
- Do not disable or weaken security controls to conceal a risk. Report the risk.
- Read-only review: do not edit code. Hand fixes to the development skill.
