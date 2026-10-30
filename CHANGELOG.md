# Changelog

## 1.2.1 — 2026-10-31

- **Roles:** role labels are now followed by smaller models too. `CLAUDE.md` gains a "Role labels" section with an example, telling the main agent to relay each subagent's result under its label instead of its own heading. Each rendered subagent description names its label, and each role file states the label at the top. In a two-role test on `claude-haiku-5-5`, labels appeared in 3 of 3 runs, against 0 of 3 with 1.2.0.

## 1.2.0 — 2026-10-31

- **Roles:** agents acting in a GADS role start each message with the role's label, for example **[Reviewer]**, so the conversation shows which role is speaking. The rule is in `AGENTS.md` and in each role file, and therefore in the rendered Claude Code subagents.
- The release workflow reports an administrator bypass of the `release` environment as a bypass, not as a missing approval. `docs/RELEASE.md` says to approve through **Review deployments** and to turn off administrator bypass.
- **Installer:** install hashes treat CRLF as LF. A Windows checkout with `core.autocrlf=true` no longer makes `repo_audit.py` report every GADS file as modified, `install.py --upgrade` write `.gads-new` files for unchanged files, or `uninstall.py` refuse. Existing `gads/install.json` files stay valid.

## 1.1.0 — 2026-10-30

- Restored the one-time repository setup for releases (environment reviewers, tag protection, tag signing) in `docs/RELEASE.md`.

Changes from the v1.1.0 validation campaign:

- **Security:** the guard hook now denies recursive deletion of `/` or `~` written with `-R`, `--recursive`, `--`, `/*`, `~/*`, quoted `"$HOME"`, or `${HOME}`, including inside subshells, command substitution, and nested `sh -c` strings. It matches Git rules when global options precede the subcommand (`git -C dir reset --hard`), asks before shell commands that touch secrets files, and fails closed on any input it cannot evaluate.
- **Security:** the Claude Code deny rules block reading `.env` and `.env.*` files in any directory, and SSH private keys.
- **Installer:** prints a warning when an existing `.claude/settings.json` leaves the guard hook inactive, and a next step when `--force` replaces `AGENTS.md` or `CLAUDE.md`. `--dry-run` shows the full plan before refusing on conflicts. The uninstaller shows how to restore backed-up instruction files.
- **Audit:** `repo_audit.py` warns when the guard hook is not wired and when replaced instruction files are still waiting in `.gads-backup-*` files.
- **Standard:** `AGENTS.md` tells agents to read `gads/PROJECT.md`, because agents that read only `AGENTS.md` (OpenCode, Codex) never see the import in `CLAUDE.md`.
- **Release tooling:** `release_report.py` launches tools by their resolved path, so npm `.cmd` tools such as `markdownlint-cli2` run on Windows.
- **CI:** updated pinned actions to `actions/checkout` 7.0.1 and `actions/setup-python` 7.1.0.
- **Adapters:** added an OpenCode adapter (`opencode.json` permission rules, validated with OpenCode 2.0.32) and a Codex page (documentation review only).

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
- Added a generic pilot checklist for evaluating adoption in a pilot repository, kept under `pilot/` separate from the standard.
- Added the optional Paperclip integration under `integrations/paperclip/`: eight GADS skills, eight role templates that wrap the canonical roles, setup and validation steps, a verified-capabilities matrix, and a governance model. The core standard does not depend on Paperclip.
- Added operating-standard sections on task decomposition, context management, and error recovery.
- Added `CODE_OF_CONDUCT.md`, `RELEASE.md`, pull request and issue templates, and a single root `CONTRIBUTING.md`.
- Release artifacts are named `global-ai-development-standard-vX.Y.Z` in the release workflow.
- Added a structural test for the Paperclip integration and fixed an upgrade test that failed on Windows line endings.
