# Global AI Development Standard (GADS)

**Version:** 1.2.0 · **Status:** Stable · **Language:** English · **Primary agent:** Claude Code

GADS is a portable operating standard for AI coding agents. It defines how an agent discovers a repository, changes it, verifies its work, and reports evidence, with clear limits on what the agent may do without a human. Git remains the source of truth for approved code and documentation.

## Why it exists

AI agents can change real projects quickly, but they do not share a common model of authority, verification, or reporting. Teams end up with ad-hoc prompts that differ per tool and per repository. GADS provides one set of rules that is written once, versioned, and checked by scripts, so each repository can adopt the same baseline.

## Design principles

1. **Repository-first:** the checked-out repository and its approved documentation are authoritative.
2. **Portable:** core rules are tool-, model-, language-, and framework-agnostic.
3. **Bounded autonomy:** agents act independently within explicit risk tiers; destructive or externally visible actions need a human.
4. **Evidence over assertion:** tests, inspections, and release reports must produce inspectable evidence.
5. **Reversible by default:** changes should be scoped, reviewable, and recoverable.
6. **Human accountability:** an agent never substitutes for an authorized human approval.
7. **No fabricated certainty:** unknowns, assumptions, and unverified checks are labelled.

## What GADS standardizes

- Agent entry point and precedence of instructions (`AGENTS.md`).
- Operating rules: discovery, change design, code quality, documentation, communication (`standard/OPERATING_STANDARD.md`).
- Risk tiers R0 to R4, approval requirements, secrets, supply chain, and prompt-injection defense (`standard/SECURITY_AND_AUTONOMY.md`).
- Lifecycle, quality gates, and completion states (`standard/WORKFLOW_AND_GATES.md`).
- Decision classes, ADR triggers, and escalation format (`standard/DECISION_POLICY.md`).
- Ten specialist roles with mission, procedure, and boundaries (`agents/`).
- Reusable reports and records: task, review, QA, ADR, lesson, and project seed (`templates/`).

## What GADS deliberately does not standardize

- Programming languages, frameworks, coding style, or architecture of a project.
- Which model, vendor, or runtime an agent uses.
- Team structure, ticketing, or project management tools.
- Branch protection, CI configuration, secrets storage, or deployment platforms. GADS describes the expectation; the repository owner configures the controls.
- Project-specific business rules. These belong in the project's own `gads/PROJECT.md`.

## Supported agent environments

| Environment | Status |
|---|---|
| **Claude Code** | Primary target. Installer renders roles as `gads-<role>` subagents, adds deny rules for secret reads, and installs a PreToolUse guard hook for risky shell commands. See [adapters/claude-code](adapters/claude-code/README.md). |
| **Generic coding agents** | Portable through `AGENTS.md` and the `standard/` documents. No adapter is shipped. See [adapters/PORTABILITY.md](adapters/PORTABILITY.md). |
| **Paperclip** (orchestration) | Optional integration with eight skills, eight role templates, and governance guidance. Capabilities are documented in [integrations/paperclip/COMPATIBILITY.md](integrations/paperclip/COMPATIBILITY.md); they are not verified against a live instance. |

## Quick start

Preview, then install into a target repository:

```bash
python scripts/install.py /path/to/target-repository --dry-run
python scripts/install.py /path/to/target-repository
```

Write project-specific rules in the created `gads/PROJECT.md` and leave the GADS-managed files unchanged, so upgrades stay clean. Then audit the installation:

```bash
python scripts/repo_audit.py /path/to/target-repository
```

Full instructions: [Installation](docs/INSTALLATION.md).

## Adopting GADS in an existing project

1. Read [standard/OPERATING_STANDARD.md](standard/OPERATING_STANDARD.md) and [standard/SECURITY_AND_AUTONOMY.md](standard/SECURITY_AND_AUTONOMY.md) with the project owner.
2. Run the installer with `--dry-run`. Resolve any conflicts with existing `AGENTS.md` or `CLAUDE.md` files; the installer never overwrites them silently.
3. Record the project's build, test, lint, and release commands in `gads/PROJECT.md`.
4. Run the installer, then `repo_audit.py`.
5. Pilot the workflow on one low-risk change using [pilot/PILOT_CHECKLIST.md](pilot/PILOT_CHECKLIST.md).

## Using GADS with Claude Code

Install GADS as above. Claude Code reads `CLAUDE.md`, which imports `AGENTS.md` and `gads/PROJECT.md`. The GADS roles are available as `gads-<role>` subagents under `.claude/agents/`. The Claude Code adapter's settings and guard hook are documented in [adapters/claude-code/README.md](adapters/claude-code/README.md).

## Using GADS with Paperclip

Paperclip orchestrates agents, tasks, and approvals; GADS defines the rules the agents follow. Start with [integrations/paperclip/README.md](integrations/paperclip/README.md), then follow [SETUP.md](integrations/paperclip/SETUP.md). Governance responsibilities by layer are in [GOVERNANCE.md](integrations/paperclip/GOVERNANCE.md).

## Validating an implementation

Run these from the GADS repository. They are local, structural checks.

```bash
python scripts/verify_manifest.py
python -m unittest discover -s tests -v
python scripts/repo_audit.py /path/to/target-repository
```

For release evidence, copy `scripts/example-release-report.json`, replace every `REPLACE_WITH_...` value, and run:

```bash
python scripts/release_gate.py path/to/release-report.json
```

The example report is intentionally unfilled and must fail the gate. A passing gate means the report is structurally complete; it does not authenticate the evidence.

## Repository layout

| Path | Contents |
|---|---|
| `AGENTS.md`, `CLAUDE.md` | Entry points for coding agents. |
| `standard/` | The authoritative normative policies. |
| `agents/` | Portable role definitions (one file per role). |
| `templates/` | Engineering artifacts, including the `PROJECT.md` seed. |
| `adapters/` | Runtime-specific files, currently Claude Code. |
| `integrations/` | Optional orchestration integrations, currently Paperclip. |
| `scripts/` | Standard-library Python utilities: installer, uninstaller, audit, manifest, release tools. |
| `tests/` | Automated tests for the scripts, links, and integration structure. |
| `docs/` | Installation, operations, troubleshooting, and release procedure. |
| `pilot/` | Pilot-evaluation material. It is not part of the standard. |
| `.github/` | CI workflows, release workflow, and contribution templates. |
| `MANIFEST.json` | SHA-256 checksums for every file except itself, checked by `scripts/verify_manifest.py`. |

## Versioning and distribution

GADS uses semantic versioning. Consumers should pin a release tag or immutable commit SHA; do not consume a moving branch in production workflows. Changes are recorded in [CHANGELOG.md](CHANGELOG.md). The release procedure is in [docs/RELEASE.md](docs/RELEASE.md). See also [versioning and upgrades](docs/OPERATIONS.md#versioning-and-upgrades).

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md). Open an issue before proposing a policy change.

## Security

Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).

## Important limitations

The scripts perform local structural checks. They do not prove that evidence is truthful, that a reviewer is independent, or that a release is secure. Repository owners remain responsible for access control, branch protection, secrets management, and approval policy.

## License

Licensed under the [Apache License 2.0](LICENSE).
