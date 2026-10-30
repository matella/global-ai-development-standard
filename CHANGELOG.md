# Changelog

## 1.0.0 — 2026-10-30

- Initial portable GADS release.
- Defined repository-first operating, security, workflow, and decision policies.
- Added ten specialist role definitions with portable frontmatter and concrete procedures, and reusable engineering templates.
- Added read-only repository audit, release evidence gate, installer, uninstaller, and unit tests.
- Installer places policies, roles, and templates under `gads/`, rewrites Markdown references, and backs up modified files on `--force`.
- Installer records hashes in `gads/install.json` and supports `--dry-run` and `--upgrade`; upgrades keep local edits and write `.gads-new` files for a manual merge.
- Added the project-owned `gads/PROJECT.md`, created once and never overwritten or removed.
- Added the Claude Code adapter: rendered `gads-<role>` subagents, secret-read deny rules, and a PreToolUse guard hook for R3/R4 commands.
- Uninstaller removes only recorded files and checks every file before removing anything.
- Release gate requires a full commit SHA, `skipped_checks`, and `approvals`, and rejects unfilled placeholders.
- Added `MANIFEST.json` verification, an install-audit-uninstall integration test, and a pinned, read-only CI matrix (Python 3.15).
- Added Apache-2.0 `LICENSE` and `SECURITY.md`.
- Added a tag-triggered release workflow: environment approval, generated release report, release gate, archives with checksums, and build provenance attestation.
- Added ruff and markdownlint CI checks, an internal documentation link test, and Dependabot updates for pinned actions.
- Added Claude Code and generic agent portability guidance.
- Added a generic pilot checklist for evaluating adoption in a pilot repository.
