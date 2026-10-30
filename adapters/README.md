# Agent adapters

Keep agent-specific configuration thin. The normative policy remains in `AGENTS.md` and `standard/`. Avoid duplicating rules across adapter files; link to the canonical policy instead.

Installed repositories place `standard/`, `agents/`, and `templates/` under `gads/`. See [PORTABILITY.md](PORTABILITY.md) for how roles reach each agent.

| Adapter | Status |
|---|---|
| [claude-code](claude-code/README.md) | Installed by `install.py`; validated with a live runtime |
| [opencode](opencode/README.md) | Manual copy of `opencode.json`; permission rules validated with a live runtime |
| [codex](codex/README.md) | Documentation review only; runtime validation outstanding |
