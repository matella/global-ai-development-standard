# Paperclip Compatibility

This file records what was verified about Paperclip, from where, and what was not verified. GADS does not depend on Paperclip; this integration is optional.

## Verification basis

- **Date:** 2026-10-30.
- **Sources:** documentation and source snippets of the open-source repository `paperclipai/paperclip` (`master` branch), retrieved through the Context7 documentation index (library `/paperclipai/paperclip`). Paths cited below refer to that repository.
- **Not verified:** no Paperclip instance was run, no API call was made, and no agent was created. Direct inspection of the pinned release notes and a live test instance remain outstanding.
- **Paperclip version tested:** none. The documentation index lists `v2026.325.0`, which was not checked against the snippets below.

## Verified capabilities

| Area | Capability | Source (paperclipai/paperclip) | Status |
|---|---|---|---|
| Agent instructions | Agent definitions carry an instructions bundle with an `entryFile` (for example `AGENTS.md`) and file contents. | `docs/companies/companies-spec.md`; `POST /api/companies/:companyId/agent-hires` in `skills-releases/…/workflows.md` and `skills/paperclip-create-agent/references/api-reference.md` | Verified from docs |
| Instructions path | `PATCH /api/agents/{agentId}/instructions-path` sets the instructions file path. Relative paths resolve against `adapterConfig.cwd`. | `skills-releases/paperclip/v0/references/workflows.md` | Verified from docs |
| Skills | A skill is a directory with `SKILL.md` (YAML frontmatter) and optional `references/`. Agents reference skills by shortname; resolution prefers `skills/<shortname>/SKILL.md`. | `docs/guides/agent-developer/writing-a-skill.md`; `docs/companies/companies-spec.md` | Verified from docs |
| Skill assignment | Hire requests accept `desiredSkills` (skill ids, canonical keys, or unique slugs). | `skills/paperclip-create-agent/references/api-reference.md` | Verified from docs |
| Skill sync | Skill management is adapter-dependent. Adapters may expose `listSkills`, `applySkills`, and sync state, or be read-only. | `doc/plans/2026-03-13-company-import-export-v2.md` (planning document) | Planned; do not assume it is implemented in every version |
| claude_local adapter | Config fields include `cwd`, `model`, `promptTemplate`, `maxTurnsPerRun`, `timeoutSec`, `env`, `extraArgs`, plus scope settings `filesystemScope` and `networkScope` (disabled by default). | `doc/spec/agent-runs.md` | Verified from docs |
| claude_local skills | The adapter creates a temporary directory of symlinks to Paperclip skills and passes it with `--add-dir`. | `docs/adapters/claude-local.md` | Verified from docs |
| claude_local settings | Remote runs sanitize the seeded Claude settings: hooks and MCP servers are removed and the permission mode is reset to default. | `packages/adapters/claude-local/src/server/claude-config.ts` | Verified from source |
| Approvals: hiring | When company settings require it, a hire creates a `hire_agent` approval and the agent is `pending_approval`. Approval is granted with `POST /api/approvals/{id}/approve`. | `skills/paperclip-create-agent/references/api-reference.md`; `skills/paperclip-board/SKILL.md` | Verified from docs |
| Approvals: board requests | Agents can file `request_board_approval` with title, summary, recommended action and risks, linked to issues. The requester is woken with `PAPERCLIP_APPROVAL_ID` and `PAPERCLIP_APPROVAL_STATUS`. | `skills/paperclip/SKILL.md` | Verified from docs |
| Heartbeat and budget | `runtimeConfig.heartbeat` (enabled, intervalSec, wakeOnDemand) and `budgetMonthlyCents`. | `skills/paperclip-create-agent/references/api-reference.md`; `skills/paperclip-board/SKILL.md` | Verified from docs |
| GitHub integration | Not verified. No GitHub-specific Paperclip configuration was checked. | — | Unverified |
| Protected branches, CI gating, environment approval | These are GitHub settings, not Paperclip features. Not verified as Paperclip capabilities. | — | Not applicable |

## What GADS relies on

GADS needs only the following from a runtime, and treats everything else as optional:

1. The agent can read a checked-out repository at `cwd` and can read the instructions file.
2. The agent can run local shell commands for the GADS scripts (Python 3 standard library).
3. Skills are readable as Markdown files, either through Paperclip's skill mechanism or from the repository itself.

## Known limitations

- **Skill installation differs by adapter.** Verify, for each adapter, how skills reach the agent before relying on them. Where skills are not available, the agent can read the same content from `integrations/paperclip/skills/` in the repository.
- **Entry-file location.** Installed repositories keep GADS policy under `gads/`. Skill and role text uses GADS-root paths (`standard/…`); in an installed repository, prefix them with `gads/`, as `scripts/repo_audit.py` does.
- **Permission and sandbox settings** are adapter-specific. GADS's guard hook and deny rules apply only where the Claude Code adapter runs the installed `.claude/settings.json`. Paperclip's sanitization of remote settings may remove hooks; verify the guard is active before trusting it.
- **Governance is not enforced by GADS.** GADS checks structure and records evidence. Access control, approvals, and branch protection must be configured in Paperclip and in the Git host. See [GOVERNANCE.md](GOVERNANCE.md).

## Versioning

This integration was introduced in GADS 1.0.0 and is unchanged since. It changes no normative policy in `standard/`. A future Paperclip change that breaks a verified row above requires an update to this file and a changelog entry.
