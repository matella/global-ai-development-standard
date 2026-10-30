#!/usr/bin/env python3
"""Install or upgrade GADS policy files in a target repository."""
import argparse
import time
from pathlib import Path

from gads_layout import (
    CREATE_ONLY,
    LOCK,
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
    if conflicts:
        p.error("destinations exist (use --force after review; originals are backed up): "
                + ", ".join(conflicts))
    prefix = "Would: " if args.dry_run else ""
    for action, rel, _ in actions:
        if action != "unchanged" or args.dry_run:
            print(prefix + MESSAGES[action].format(rel=rel, source=f"adapters/claude-code/{Path(rel).name}"))
    if args.dry_run:
        return 0
    apply(target, actions, time.strftime("%Y%m%d%H%M%S"))
    write_lock(target, recorded)
    print(f"GADS {version()} recorded in {LOCK}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
