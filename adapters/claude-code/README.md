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
  `~`, including `-R`, `--recursive`, `/*`, `~/*`, `$HOME`, and `${HOME}` targets, inside subshells,
  `$(...)`, backticks, and nested `bash -c "..."` strings. Long options count by unambiguous prefix,
  as GNU `rm` reads them: `--recur` and `--rec` are `--recursive`. An `rm` of `/` or `~` with a long
  option the guard does not recognise, such as `--re`, gets an "ask" decision. The check is
  conservative: it also denies a command that only prints such text, for example `echo "rm -rf /"`.
- The hook fails closed: an event it cannot evaluate gets an "ask" decision.
- The hook command in `.claude/settings.json` starts the guard with the first working Python 3 among
  `python3`, `python`, and `py -3`. Each candidate is test-run first, so the Windows Store
  `python3` alias that exists but cannot run is skipped. If no interpreter works, or the guard itself
  fails, the command exits with code 2, which makes Claude Code block the tool call and show the
  reason. Any other failure to start would count as a non-blocking hook error, and Claude Code would
  run the command without the guard. Without Python 3, every Bash call is blocked until one is
  installed.
- The launcher is inline in `settings.json`, not a separate `.sh` file, so a CRLF checkout cannot
  break it. Claude Code runs hook commands through a POSIX shell (Git Bash on Windows).
- Projects that merged the 1.3.0 `python3 ".../guard_bash.py"` command by hand should replace it with
  the current command; the old one fails open on machines without `python3`.
- In a non-interactive session (`claude -p --permission-mode dontAsk`), an "ask" decision becomes a
  denial. Interactive sessions show the approval prompt.
- Pattern matching is a safety net, not a security boundary. Keep branch protection, required
  reviews, and least-privilege credentials in place.
