# Operations

## Daily use

- Keep policy in version control.
- Review instruction changes like code.
- Re-run tests and repository audit after upgrades.
- Capture durable decisions in ADRs.
- Keep agent permissions least-privileged.

## Versioning and upgrades

Pin a release tag (for example `v1.0.0`) or immutable commit SHA. Avoid tracking `main` for operational use. Upgrade with `install.py --upgrade` (see [Installation](INSTALLATION.md#upgrade)). Read the changelog, compare policy changes, run the included tests, and pilot upgrades on a non-critical repository before broad rollout (see the [pilot checklist](../pilot/PILOT_CHECKLIST.md)).

## Governance

Assign a human owner for policy changes. Use pull requests, required reviewers, protected branches, and signed releases where appropriate. The kit does not configure these controls automatically. For how instructions, automated controls, approvals, and evidence fit together, see [GOVERNANCE.md](../integrations/paperclip/GOVERNANCE.md).

## Release evidence

Use `scripts/release_gate.py` against a JSON report based on `scripts/example-release-report.json`. Required fields:

- `version`, `commit` (full SHA), `rollback_plan`: non-empty strings.
- `checks`: non-empty list of `{name, status}`; status `passed` or `not_applicable`.
- `skipped_checks`: list of `{name, reason}`.
- `approvals`: list of `{action, approver}`.
- `known_risks`: list of strings.

The script rejects unfilled `REPLACE_WITH_...` values. It checks structure only; it does not verify the underlying evidence or approval identity.

`scripts/release_report.py` builds the report from real check runs instead of hand-written results. Checks whose tool is missing are listed in `skipped_checks`. Without `--approver`, the approver stays a placeholder and the gate fails.

## Publishing a release

The procedure, including the approval step, rollback, and artifact verification, is in [RELEASE.md](RELEASE.md).
