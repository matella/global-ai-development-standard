# Installation

## Requirements

- Python 3.15 or newer for the included scripts (the most recent Python release, supported until October 2031).
- Git repository with a clean understanding of existing local changes.
- Write access to the target repository.

## Install

Preview, then install:

```bash
python scripts/install.py /path/to/target-repository --dry-run
python scripts/install.py /path/to/target-repository
```

| Kit source | Installed path | Owner |
|---|---|---|
| `AGENTS.md` | `AGENTS.md` | GADS |
| `CLAUDE.md` | `CLAUDE.md` (imports `@AGENTS.md` and `@gads/PROJECT.md`) | GADS |
| `standard/`, `agents/`, `templates/` | `gads/standard/`, `gads/agents/`, `gads/templates/` | GADS |
| `agents/<role>.md` | `.claude/agents/gads-<role>.md` (rendered subagent) | GADS |
| `adapters/claude-code/settings.json` | `.claude/settings.json` (only when absent) | GADS |
| `adapters/claude-code/hooks/guard_bash.py` | `gads/hooks/guard_bash.py` | GADS |
| `templates/PROJECT.md` | `gads/PROJECT.md` | Project |

Markdown references to `standard/`, `agents/`, and `templates/` are rewritten to their `gads/` paths.

The installer records the version and the SHA-256 of every file it writes in `gads/install.json`. Commit that file with the others.

Existing files block the install unless `--force` is supplied. With `--force`, each differing file is first renamed to `<name>.gads-backup-<timestamp>`. An existing `.claude/settings.json` is never replaced; merge its entries by hand (see [Claude Code adapter](../adapters/claude-code/README.md)).

Verify the result:

```bash
python scripts/repo_audit.py /path/to/target-repository
```

## Project-specific rules

Write project rules in `gads/PROJECT.md`, not in the GADS-managed files. The installer creates it once and never overwrites or removes it. Claude Code imports it through `CLAUDE.md`; `AGENTS.md` names it for other agents.

## Upgrade

Check out the new kit version (a pinned tag), then:

```bash
python scripts/install.py /path/to/target-repository --upgrade --dry-run
python scripts/install.py /path/to/target-repository --upgrade
```

The upgrade compares each file with the hash recorded at install time:

- unmodified files are replaced with the new version;
- locally modified files are kept, and the new version is written beside them as `<name>.gads-new` for a manual merge;
- unmodified files that the new version no longer ships are removed.

`gads/PROJECT.md` is never touched. Review the diff before committing.

## Manual installation

Follow the table above, rewrite the references, and adapt project-specific rules in `gads/PROJECT.md`. Without `gads/install.json`, the upgrade and uninstall commands are unavailable.

## Uninstall

```bash
python scripts/uninstall.py /path/to/target-repository --dry-run
python scripts/uninstall.py /path/to/target-repository
```

The uninstaller removes only the files listed in `gads/install.json`. It checks every file first. If any file changed since install, it removes nothing unless `--force` is supplied. `--force` also removes those local edits, so back them up first. `gads/PROJECT.md`, a `.claude/settings.json` edited by the project (even with `--force`), backups, and `.gads-new` files are kept.
