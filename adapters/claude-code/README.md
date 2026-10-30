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
  skips it, even with `--force`, and prints a warning that the guard is not active. Merge the
  `permissions.deny` and `hooks` entries by hand. `repo_audit.py` warns until the hook is wired.
- The deny rules block the `Read` tool on `.env` and `.env.*` files in any directory (including
  `.env.example`), `*.pem`, `*.key`, and SSH private keys.
- The hook asks for human approval before force-push, remote ref or tag deletion or publication,
  history rewrites, discarding local work, GitHub release and repository changes, package publication,
  infrastructure changes, piping remote scripts to a shell, and shell commands that touch secrets
  files (`.env*` except `.env.example`, `*.pem`, `*.key`, SSH keys). Git rules also match when global
  options precede the subcommand (`git -C dir reset --hard`). It denies recursive deletion of `/` or
  `~`, including `-R`, `--recursive`, `/*`, `~/*`, `$HOME`, and `${HOME}` targets.
- The hook fails closed: an event it cannot evaluate gets an "ask" decision.
- The hook runs `python3`. If `python3` is missing (common on Windows), Claude Code reports a hook
  error and runs the command without the guard; no change inside the script can prevent that.
  Check with `python3 --version`, and adjust the command in `.claude/settings.json` if needed.
- In a non-interactive session (`claude -p --permission-mode dontAsk`), an "ask" decision becomes a
  denial. Interactive sessions show the approval prompt.
- Pattern matching is a safety net, not a security boundary. Keep branch protection, required
  reviews, and least-privilege credentials in place.
