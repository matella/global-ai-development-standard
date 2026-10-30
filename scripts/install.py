#!/usr/bin/env python3
"""Install or upgrade GADS policy files in a target repository."""
import argparse
import time
from pathlib import Path

from gads_layout import (
    CREATE_ONLY,
    LOCK,
    ROOT_FILES,
    current_hash,
    plan,
    prune_empty_dirs,
    read_lock,
    seeds,
    sha256,
    version,
    write_lock,
)


def decide(target, lock, force):
    """Return (actions, recorded, conflicts) without touching the target."""
    files, previous = plan(), (lock or {}).get("files", {})
    actions, recorded, conflicts = [], {}, []
    for rel, data in files.items():
        new, cur, old = sha256(data), current_hash(target / rel), previous.get(rel)
        if cur is None:
            actions.append(("write", rel, data))
        elif cur == new:
            actions.append(("unchanged", rel, None))
        elif old is not None and cur == old:
            actions.append(("update", rel, data))
        elif old is not None:
            # Locally modified since the last install: keep it, offer the new version beside it.
            actions.append(("merge", rel, data))
            recorded[rel] = old
            continue
        elif rel in CREATE_ONLY:
            actions.append(("skip", rel, None))
            continue
        elif force:
            actions.append(("backup", rel, data))
        else:
            conflicts.append(rel)
        recorded[rel] = new
    for rel, old in previous.items():
        if rel not in files:
            cur = current_hash(target / rel)
            if cur == old:
                actions.append(("remove", rel, None))
            elif cur is not None:
                actions.append(("orphan", rel, None))
    for rel, data in seeds().items():
        actions.append(("keep" if (target / rel).exists() else "seed", rel, data))
    return actions, recorded, conflicts


MESSAGES = {
    "write": "Installed {rel}", "update": "Updated {rel}", "unchanged": "Unchanged {rel}",
    "backup": "Backed up and replaced {rel}", "seed": "Created project-owned {rel}",
    "keep": "Kept project-owned {rel}", "remove": "Removed {rel} (no longer in the kit)",
    "orphan": "Kept {rel}: modified locally and no longer managed by GADS",
    "merge": "Kept {rel}: modified locally; review {rel}.gads-new and merge by hand",
    "skip": "Skipped {rel}: it already exists; merge {source} by hand",
}


def apply(target, actions, stamp):
    for action, rel, data in actions:
        path = target / rel
        if action == "backup":
            path.rename(path.with_name(f"{path.name}.gads-backup-{stamp}"))
        elif action == "merge":
            path = path.with_name(f"{path.name}.gads-new")
        elif action == "remove":
            path.unlink()
            prune_empty_dirs(target, rel)
        if action in {"write", "update", "backup", "merge", "seed"}:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("target")
    p.add_argument("--upgrade", action="store_true", help="upgrade an existing installation")
    p.add_argument("--force", action="store_true",
                   help="replace existing unmanaged files after backing them up")
    p.add_argument("--dry-run", action="store_true", help="print planned actions only")
    args = p.parse_args(argv)
    target = Path(args.target).resolve()
    if not target.is_dir():
        p.error(f"target directory does not exist: {target}")
    lock = read_lock(target)
    if lock and not args.upgrade:
        p.error(f"GADS {lock.get('version')} is already installed; use --upgrade")
    if args.upgrade and not lock:
        p.error(f"no {LOCK} found; run a fresh install first")
    actions, recorded, conflicts = decide(target, lock, args.force)
    prefix = "Would: " if args.dry_run else ""
    if conflicts and not args.dry_run:
        p.error("destinations exist (use --force after review; originals are backed up): "
                + ", ".join(conflicts))
    for action, rel, _ in actions:
        if action != "unchanged" or args.dry_run:
            print(prefix + MESSAGES[action].format(rel=rel, source=f"adapters/claude-code/{Path(rel).name}"))
    if conflicts:
        # Dry run: show the whole plan first, then refuse as the real run would.
        p.error("destinations exist (use --force after review; originals are backed up): "
                + ", ".join(conflicts))
    stamp = time.strftime("%Y%m%d%H%M%S")
    if not args.dry_run:
        apply(target, actions, stamp)
        write_lock(target, recorded)
        print(f"GADS {version()} recorded in {LOCK}")
    for note in next_steps(actions, stamp):
        print(prefix + note)
    return 0


def next_steps(actions, stamp):
    """Follow-up the project must do by hand, so safety controls and rules are not silently lost."""
    for action, rel, _ in actions:
        if action == "skip" and rel == ".claude/settings.json":
            yield ("WARNING: the GADS guard hook is NOT active. Merge `permissions.deny` and `hooks` from "
                   "adapters/claude-code/settings.json into .claude/settings.json, then run repo_audit.py.")
        elif action == "backup" and rel in ROOT_FILES:
            yield (f"NEXT STEP: {rel} was replaced. Its previous rules are now only in "
                   f"{rel}.gads-backup-{stamp} and are no longer loaded by agents. Move them into "
                   "gads/PROJECT.md, then delete the backup.")


if __name__ == "__main__":
    raise SystemExit(main())
