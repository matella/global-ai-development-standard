# Governance Model for Paperclip Deployments

Paperclip orchestrates agents, tasks, and approvals. GADS defines the rules agents follow. Git and the Git host remain the source of truth. This document separates what each layer can actually enforce.

## Four kinds of control

| Kind | What it is | Who enforces it | Examples |
|---|---|---|---|
| **Instructions** | Rules the agent is asked to follow | Nobody mechanically; relies on model compliance | `AGENTS.md`, role templates, skills, `standard/` |
| **Automated controls** | Checks a script, test, or CI job can fail | Scripts, tests, CI, the Git host | `verify_manifest.py`, `repo_audit.py`, `release_gate.py`, unit tests, GitHub branch rules |
| **Human approvals** | Decisions only an accountable person can make | People, recorded in Paperclip or the Git host | Hire approval, board approval, release approval, merge approval |
| **Evidence** | Records that show what happened | Repository, CI logs, release reports, Paperclip issue history | Commit SHA, command outcomes, approval IDs, `release-report.json` |

Rule of thumb: a critical rule must have an automated control or a human approval behind its instruction. An instruction alone is not a control.

## Recommendations by boundary

| Boundary | Instruction (agent) | Automated control | Human approval | Evidence |
|---|---|---|---|---|
| **Approval boundaries** | Stop and request approval for R3 actions (`standard/SECURITY_AND_AUTONOMY.md`) | None mechanical in GADS. Use Paperclip's board approval request where your Paperclip version provides it | Named accountable human for each R3 action | Approval record linked to the issue |
| **Protected branches** | Work on task branches; never push to `main` or release branches | Git host branch protection with required reviews and status checks. Configure outside GADS | Owners of the repository set the rules | Branch protection settings and PR history |
| **Destructive operations** | Do not delete data, force-push, or rewrite shared history | Git host rules that block force-push on protected branches. Local hooks can be bypassed and are not sufficient | Explicit approval naming the action and scope | Approval record and command log |
| **Secrets and credentials** | Never print, commit, or copy secrets | `.gitignore` for `.env` files, secret scanning on the Git host, Claude Code deny rules for secret reads (installed by GADS) | Rotation and access grants by the owner | Scanner output; no secret values in reports |
| **External communications** | Do not post to external services or send messages without approval | None in GADS. Restrict tool access in the runtime configuration | Approval for each outbound message class | Approval record |
| **Production deployments** | Do not deploy or modify production | Deployment pipeline with an environment that requires reviewers, configured outside GADS | Accountable human approves each deployment | Pipeline run and approval history |
| **Dependency changes** | Explain necessity, license, and risk before adding a dependency | Lockfile checks and dependency review in CI, configured per project | Approval for new runtime dependencies | Diff of lockfiles; decision note |
| **Release creation** | Prepare the release report; never tag or publish on its own | `release_gate.py` validates structure; `release.yml` requires environment approval before publishing | Environment reviewer approves publication | Release report, provenance attestation, approval record |

## Limits of GADS and Paperclip enforcement

- `release_gate.py` checks structure only and cannot authenticate evidence.
- The GADS guard hook runs only where the Claude Code adapter applies the installed settings. Paperclip may sanitize remote Claude settings; verify before relying on it (see [COMPATIBILITY.md](COMPATIBILITY.md)).
- This repository's `release.yml` requires a GitHub environment named `release` with required reviewers. Without it the workflow fails at the approval step. Configuring the environment is a repository-owner decision.
- Paperclip's approval endpoints are verified from documentation only (see [COMPATIBILITY.md](COMPATIBILITY.md)). Do not assume an approval gate exists for an action until it is tested in your deployment.

## Evidence to retain

- Commit SHA and tag for every change and release.
- Command outcomes in the task or QA report (passed, failed, not run, blocked).
- Approval identifiers and decision notes for each R3 action.
- Release report that passes `release_gate.py`, plus the checksums and attestation for release artifacts.
