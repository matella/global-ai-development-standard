# Portability Guide

## Core contract

Any compatible coding agent should be able to:

- read Markdown policy files from the repository;
- inspect and modify repository files;
- execute explicitly permitted local commands;
- report tool limitations and validation evidence.

## Adapter strategy

1. Keep `AGENTS.md` as the shared entry point.
2. Add a small native entry file only when the agent requires it (for example, `CLAUDE.md`).
3. Have adapters point back to canonical policies.
4. Do not encode critical policy only in a hosted agent profile or personal memory.
5. Validate behavior after changing agent versions or adapter configuration.

## Roles across agents

The canonical roles in `agents/` are agent-neutral Markdown with portable frontmatter: `name`, `description`, and `access` (`read-only` or `read-write`). They install to `gads/agents/` for every agent.

An adapter renders them into the agent's native format without copying the text by hand. The Claude Code adapter renders `.claude/agents/gads-<role>.md` and maps `access` to a tool list. To support another agent, add a renderer for its format; keep the role text in `agents/`.

Agents without native subagents can still adopt a role by reading its file in `gads/agents/`.

## Portability caveats

Different agents interpret instruction discovery, context windows, tool permissions, and subagent delegation differently. File presence does not guarantee compliance. Test each adapter in a low-risk task before relying on it.
