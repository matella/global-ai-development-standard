#!/usr/bin/env python3
"""Remove installed GADS files; files modified since install require --force."""
import argparse
from pathlib import Path

from gads_layout import CREATE_ONLY, LOCK, current_hash, prune_empty_dirs, read_lock


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("target")
    p.add_argument("--force", action="store_true",
                   help="also remove files modified since install")
    p.add_argument("--dry-run", action="store_true", help="print planned actions only")
    args = p.parse_args(argv)
    target = Path(args.target).resolve()
    if not target.is_dir():
        p.error(f"target directory does not exist: {target}")
    lock = read_lock(target)
    if not lock:
        p.error(f"no {LOCK} found; nothing was installed by GADS here")
    files = lock.get("files", {})
    present = [rel for rel in files if (target / rel).is_file()]
    # Check everything before removing anything, so a refusal leaves the target untouched.
    modified = [rel for rel in present if current_hash(target / rel) != files[rel]]
    # A project that edited a GADS-created settings file now owns it: keep it, even with --force.
    kept = [rel for rel in modified if rel in CREATE_ONLY]
    present = [rel for rel in present if rel not in kept]
    modified = [rel for rel in modified if rel not in kept]
    if modified and not args.force:
        p.error("modified since install; nothing removed (use --force after review): "
                + ", ".join(modified))
    prefix = "Would remove" if args.dry_run else "Removed"
    for rel in present + [LOCK]:
        print(f"{prefix} {rel}")
        if not args.dry_run:
            (target / rel).unlink()
            prune_empty_dirs(target, rel)
    for rel in kept:
        print(f"Kept {rel}: modified by the project")
    for rel in lock.get("seeds", []):
        if (target / rel).exists():
            print(f"Kept project-owned {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
