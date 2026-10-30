# Global AI Development Standard (GADS)

**Version:** 1.0.0  
**Status:** Initial release  
**Language:** English  
**Primary agent:** Claude Code  
**Scope:** Agent-assisted software development across languages, frameworks, repositories, and hosting environments.

GADS defines a portable operating model for AI coding agents. It separates durable repository policy from agent-specific instructions, requires evidence for consequential claims, and keeps Git as the source of truth for approved code and documentation.

## Design principles

1. **Repository-first:** the checked-out repository and its approved documentation are authoritative.
2. **Portable:** core rules are tool-, model-, language-, and framework-agnostic.
3. **Bounded autonomy:** agents may act independently within explicit risk limits.
4. **Evidence over assertion:** tests, inspections, and release gates must produce inspectable evidence.
5. **Reversible by default:** changes should be scoped, reviewable, and recoverable.
6. **Human accountability:** an agent never substitutes for an authorized human approval.
7. **No fabricated certainty:** unknowns, assumptions, and unverified checks are labelled.

## Quick start

```bash
python scripts/install.py /path/to/target-repository --dry-run
python scripts/install.py /path/to/target-repository
```

Write project-specific rules in the created `gads/PROJECT.md`; leave the GADS-managed files unchanged so upgrades stay clean. Verify the installation:

```bash
python scripts/repo_audit.py /path/to/target-repository
```

To check release evidence, copy `scripts/example-release-report.json`, replace every `REPLACE_WITH_...` value, and run:

```bash
python scripts/release_gate.py path/to/release-report.json
```

See [Installation](docs/INSTALLATION.md), [Operations](docs/OPERATIONS.md), and [Security and autonomy](standard/SECURITY_AND_AUTONOMY.md).

## Repository layout

- `standard/` — normative operating policies.
- `agents/` — portable role definitions; rendered as Claude Code subagents on install.
- `templates/` — repeatable engineering artifacts, including the `PROJECT.md` seed.
- `adapters/` — agent-specific integration; `adapters/claude-code/` holds the settings and guard hook.
- `scripts/` — portable standard-library Python utilities.
- `tests/` — automated tests for included utilities.
- `MANIFEST.json` — SHA-256 checksums, checked by `scripts/verify_manifest.py`.

## Versioning and distribution

GADS uses semantic versioning. Consumers should pin a release tag or immutable commit SHA; do not consume a moving branch in production workflows. See [versioning](docs/OPERATIONS.md#versioning-and-upgrades).

## Security

Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).

## Important limitations

The scripts perform local structural checks. They do not prove that evidence is truthful, that a reviewer is independent, or that a release is secure. Repository owners remain responsible for access control, branch protection, secrets management, and approval policy.

## License

Licensed under the [Apache License 2.0](LICENSE).
