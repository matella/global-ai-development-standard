# Paperclip Integration

This optional integration lets [Paperclip](https://paperclip.ing/docs) orchestrate AI agents that work under the Global AI Development Standard (GADS). GADS does not depend on Paperclip, and nothing in `standard/` mentions it.

## Architecture

| Layer | Responsibility |
|---|---|
| **GADS** | Development rules, governance, quality, security, and workflows (`standard/`, `agents/`, `templates/`) |
| **Paperclip** | Orchestration: agent definitions, task assignment, budgets, heartbeats, and approvals |
| **Runtime** (for example Claude Code) | Performs the development work inside a checked-out repository |
| **Git** | Source of truth for code and approved documentation |

Paperclip assigns work and records approvals. It does not define what the agent may do. The rules come from the GADS documents that the agent reads from the repository.

## Contents

| Path | Purpose |
|---|---|
| [SETUP.md](SETUP.md) | Installation, agent creation, and validation steps |
| [COMPATIBILITY.md](COMPATIBILITY.md) | Verified Paperclip capabilities, sources, limitations |
| [GOVERNANCE.md](GOVERNANCE.md) | Instructions, automated controls, approvals, and evidence |
| [skills/](skills/) | Eight GADS skills in `SKILL.md` format: core, development, architecture, code review, testing and QA, security review, documentation, release management |
| [roles/](roles/) | Eight role templates for Paperclip agent instructions, each pointing to a canonical GADS role |
| [examples/](examples/) | Example agent-hire request body (not executed in CI) |

## Design rules

- **One source of truth.** Role templates wrap `agents/*.md` and skills reference `standard/*.md`. Neither copies policy text.
- **No new core roles.** Security Reviewer and Documentation Specialist are composed from `agents/reviewer.md` and `agents/librarian.md` plus their skills. Core roles are unchanged.
- **Honest scope.** Each Paperclip capability used here is listed in [COMPATIBILITY.md](COMPATIBILITY.md) with its source and verification status.

## Status

Structure and content are validated by `tests/test_paperclip_integration.py`. The Paperclip behavior described here has **not** been run against a live Paperclip instance. Treat [COMPATIBILITY.md](COMPATIBILITY.md) as the authority on what is verified.
