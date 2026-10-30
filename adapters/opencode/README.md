# OpenCode adapter

OpenCode reads `AGENTS.md` and does not use `CLAUDE.md`, so the Claude Code guard hook and deny rules do not apply. This adapter supplies the equivalent controls as OpenCode permission rules.

## Install

The GADS installer does not write OpenCode files. After `install.py`, copy [opencode.json](opencode.json) to the repository root. If the project already has an `opencode.json`, merge the `instructions` and `permission` entries by hand.

| Entry | Purpose |
|---|---|
| `instructions: ["gads/PROJECT.md"]` | Loads the project rules, which OpenCode would otherwise reach only by reading `AGENTS.md` and opening the file |
| `permission.bash` | Allows routine read, test, and local Git commands; asks for anything else; denies GADS R3/R4 commands |
| `permission.read` | Denies reading `.env` files and private keys |
| `permission.webfetch` | Denies web fetches; enable per project when needed |

Extend the `bash` allow list with the project's own build and test commands, for example `"bun run test*": "allow"`.

## Behavior to know

- OpenCode evaluates rules in order and the **last matching rule wins**, so the catch-all `"*"` comes first and the R3 denials come last.
- `opencode run --auto` approves every rule that is not explicitly denied, including `ask`. That is why R3/R4 commands are `deny`, not `ask`: an `ask` rule offers no protection in auto-approve automation.
- Without `--auto`, a headless `opencode run` rejects unanswered `ask` requests.
- A denial reports only `Permission denied: shell`, without the GADS reason. The agent sees that it was blocked, not why.
- Any allowed interpreter or test runner can execute code the agent wrote, so command denials are a safety net, not a sandbox. The file allows only `python -m unittest`, `python -m pytest`, and `python scripts/*`, never a general `python *`. For unattended automation, consider `"*": "deny"` as the catch-all.
- Git R3 rules are repeated as `git -* ...` so that global options (`git -C dir push`) do not evade them, and `sudo`, `env`, and `command` wrappers are denied.

## Validation

Validated with OpenCode 2.0.32 on Windows on 2026-10-30, in throwaway test repositories (GADS validation campaign), using an earlier version of this file with the same R3/R4 `deny` rules and a shorter allow list:

- `git reset --hard` and `git push --force origin main` were denied before execution; the remote was unchanged.
- Allow-listed commands (`python -m unittest`, `git checkout -b`, `git commit`) ran.
- Unlisted commands, including compound status commands built with `echo`, were requested and auto-rejected in headless mode.

The read-only utilities in the allow list (`echo`, `head`, `tail`, `wc`, `grep`, Git queries) and the shell-level secret denials (`* .env`, `* *.pem*`, ...) were added afterwards. They are covered by `tests/test_opencode_adapter.py` but have **not** been re-run against a live OpenCode session. The `.env.*` denials also block `.env.example`.

Not validated: the current file in a live session, interactive approval prompts, other OpenCode versions, and `--auto` mode. Pattern rules are a safety net, not a security boundary; keep branch protection and least-privilege credentials in place.
