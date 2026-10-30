# Claude Code adapter

The installer derives these files from the portable kit. Do not edit the installed copies; change the
kit and run `install.py --upgrade`.

| Installed path | Source | Purpose |
|---|---|---|
| `CLAUDE.md` | `CLAUDE.md` | Imports `@AGENTS.md` and `@gads/PROJECT.md` |
| `.claude/agents/gads-<role>.md` | `agents/<role>.md` | Subagents rendered from the canonical roles |
| `.claude/settings.json` | `adapters/claude-code/settings.json` | Secret-read deny rules and the Bash guard hook |
| `gads/hooks/guard_bash.py` | `adapters/claude-code/hooks/guard_bash.py` | PreToolUse guard for R3/R4 commands |

## Subagents

Each canonical role declares a portable `access` level. The adapter maps it to Claude Code tools:

| `access` | Claude Code `tools` |
|---|---|
| `read-only` | `Read, Grep, Glob, Bash` (no `Edit` or `Write`) |
| `read-write` | All tools (field omitted) |

`Bash` stays available to read-only roles so they can run `git diff` and tests. The role text forbids
edits; the tool list cannot enforce that through `Bash`.

## Settings and guard hook

- `.claude/settings.json` is created only when absent. If the project already has one, the installer
  skips it, even with `--force`. Merge the `permissions.deny` and `hooks` entries by hand.
- The hook asks for human approval before force-push, remote ref or tag deletion or publication,
  history rewrites, discarding local work, GitHub release and repository changes, package publication,
  infrastructure changes, and piping remote scripts to a shell. It denies recursive deletion of `/`
  or `~`.
- The hook runs `python3`. If `python3` is missing (common on Windows), Claude Code reports a hook
  error and runs the command without the guard. Adjust the command in `.claude/settings.json`.
- Pattern matching is a safety net, not a security boundary. Keep branch protection, required
  reviews, and least-privilege credentials in place.
