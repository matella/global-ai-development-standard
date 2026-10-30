# Paperclip Setup and Validation

This procedure connects a repository that follows GADS to agents managed by [Paperclip](https://paperclip.ing/docs). Read [README.md](README.md) first for the architecture, and [COMPATIBILITY.md](COMPATIBILITY.md) for which steps are verified.

## 1. Prepare the repository

1. Check out the GADS release tag you intend to use, for example `v1.0.0`. Do not track `main` (see [OPERATIONS.md](../../docs/OPERATIONS.md#versioning-and-upgrades)).
2. Install GADS into the target repository. Preview first:

   ```bash
   python scripts/install.py /path/to/target-repository --dry-run
   python scripts/install.py /path/to/target-repository
   ```

   The installer writes `AGENTS.md`, `CLAUDE.md`, `gads/`, and `.claude/agents/`, and creates the project-owned `gads/PROJECT.md`. Record project rules there.
3. Audit the installation:

   ```bash
   python scripts/repo_audit.py /path/to/target-repository
   ```

   Expect no `FAIL` lines. Investigate any `WARNING` before the agent runs.

## 2. Make the skills available

Each directory under `integrations/paperclip/skills/` is a self-contained skill (`SKILL.md` with frontmatter). Register them with Paperclip using the skill mechanism your Paperclip version supports (see the skill sections of [COMPATIBILITY.md](COMPATIBILITY.md)). Reference them by shortname, for example `gads-core`.

## 3. Create the agent

Choose a role template from `integrations/paperclip/roles/`. Use the agent-hire request shape in `examples/hire-qa-engineer.example.json` as a guide:

- `adapterConfig.cwd` must be the absolute path of the checked-out repository.
- `instructionsBundle.files["AGENTS.md"]` holds the role template contents, with `entryFile` set to `AGENTS.md`.
- `desiredSkills` lists the skills from the role template header.
- Keep `budgetMonthlyCents` and heartbeat settings deliberately small for the first run.
- Do not enable permission bypass options (for example `dangerouslySkipPermissions`). Rely on the GADS Claude Code adapter guard and deny rules installed in step 1.

If the company requires approval for new agents, the hire returns a `pending_approval` status and an approval record. An accountable human must approve it.

## 4. Validate the first run

Run a bounded task in a test repository first, then a real one. Check that:

- The agent reads `AGENTS.md` and the `gads/standard/` documents before editing.
- Its report lists commands with passed, failed, not run, or blocked outcomes.
- It does not run R3 actions (publishing, pushing to protected branches, deleting data) without an approval.
- `repo_audit.py` still passes after the run and `git status` shows only the intended changes.

Record the result as a pilot observation using [pilot/PILOT_CHECKLIST.md](../../pilot/PILOT_CHECKLIST.md).

## 5. Upgrade or remove

- Upgrade: check out the new tag, then run `python scripts/install.py <repo> --upgrade`. Review `.gads-new` files that the installer writes for locally modified files.
- Remove: `python scripts/uninstall.py <repo>`. It removes only recorded GADS files. Remove the Paperclip agent and skills separately in Paperclip.
