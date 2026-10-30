# Codex adapter

**Status: documentation review only.** No Codex runtime was available for the GADS validation campaign. Nothing on this page has been tested by running Codex.

## Instruction discovery

According to the Codex documentation (`openai/codex`, `rust-v0.155.1`), Codex includes the repository-root `AGENTS.md` and every `AGENTS.md` from the working directory up to the root in its context. More deeply nested files take precedence, and direct user instructions take precedence over `AGENTS.md`.

GADS therefore needs no Codex-specific entry file. `AGENTS.md` tells agents to read `gads/PROJECT.md`, because Codex does not process the `@gads/PROJECT.md` import in `CLAUDE.md`.

## Safety controls

The Claude Code guard hook and deny rules do not apply to Codex. Codex controls command execution through its own sandbox and approval policy, for example in `~/.codex/config.toml`:

```toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = false
```

With `workspace-write`, edits outside the working directory need approval. Map GADS risk tiers onto these settings conservatively, and keep branch protection on the Git host, since prompt-level rules alone are not a control.

## Roles

Codex has no renderer for the GADS roles. An agent adopts a role by reading its file under `gads/agents/`.

## Outstanding validation

Run the GADS validation scenarios (instruction discovery, a scoped feature task, a destructive-command request, an embedded-approval injection, a secret commit request) with a pinned Codex version before claiming compatibility.
