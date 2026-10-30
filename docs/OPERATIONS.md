# Operations

## Daily use

- Keep policy in version control.
- Review instruction changes like code.
- Re-run tests and repository audit after upgrades.
- Capture durable decisions in ADRs.
- Keep agent permissions least-privileged.

## Versioning and upgrades

Pin a release tag (for example `v1.0.0`) or immutable commit SHA. Avoid tracking `main` for operational use. Upgrade with `install.py --upgrade` (see [Installation](INSTALLATION.md#upgrade)). Read the changelog, compare policy changes, run the included tests, and pilot upgrades on a non-critical repository before broad rollout (see the [pilot checklist](PILOT_CHECKLIST.md)).

## Governance

Assign a human owner for policy changes. Use pull requests, required reviewers, protected branches, and signed releases where appropriate. The kit does not configure these controls automatically.

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

Pushing a `v*` tag runs `.github/workflows/release.yml`. The workflow:

1. checks that the tag matches `VERSION`;
2. waits for approval on the `release` GitHub environment;
3. records the approving reviewers from the run's approval history;
4. generates the release report and runs the release gate;
5. builds zip and tar.gz archives with `SHA256SUMS`;
6. attests build provenance for the archives;
7. creates the GitHub release with the changelog section as notes.

One-time setup by a repository administrator:

- create the `release` environment with required reviewers, and restrict it to `v*` tags;
- protect `v*` tags against deletion and update;
- sign release tags (`git tag -s`) with a key registered on GitHub.

Consumers can verify an archive with `gh attestation verify <archive> --repo <owner>/global-ai-development-standard`.
