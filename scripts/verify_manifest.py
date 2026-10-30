#!/usr/bin/env python3
"""Verify, or regenerate with --write, the SHA-256 checksums in MANIFEST.json."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "MANIFEST.json"
# .github is excluded so Dependabot SHA bumps do not break verification; git and
# release provenance cover it, and it is never installed into consumers.
EXCLUDED_DIRS = {".git", ".github", "__pycache__", ".pytest_cache", ".ruff_cache", ".venv", "venv", "node_modules"}
# Per-developer files that .gitignore keeps out of the repository.
EXCLUDED_FILES = {".claude/settings.local.json"}


def collect(root):
    files = {}
    for f in sorted(root.rglob("*")):
        rel = f.relative_to(root)
        if (f.is_file() and rel.as_posix() not in EXCLUDED_FILES | {MANIFEST}
                and not EXCLUDED_DIRS.intersection(rel.parts)):
            files[rel.as_posix()] = hashlib.sha256(f.read_bytes()).hexdigest()
    return files


def verify(root):
    manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    listed, actual = manifest.get("files", {}), collect(root)
    errors = [f"checksum mismatch: {f}" for f in sorted(listed) if f in actual and actual[f] != listed[f]]
    errors += [f"listed but missing: {f}" for f in sorted(set(listed) - set(actual))]
    errors += [f"present but unlisted: {f}" for f in sorted(set(actual) - set(listed))]
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if manifest.get("version") != version:
        errors.append(f"manifest version {manifest.get('version')!r} differs from VERSION {version!r}")
    return errors


def write(root):
    path = root / MANIFEST
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["version"] = (root / "VERSION").read_text(encoding="utf-8").strip()
    manifest["files"] = collect(root)
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("root", nargs="?", default=str(ROOT))
    p.add_argument("--write", action="store_true", help="regenerate checksums instead of verifying")
    args = p.parse_args(argv)
    root = Path(args.root).resolve()
    if args.write:
        write(root)
        print(f"Wrote {MANIFEST}")
        return 0
    errors = verify(root)
    if errors:
        print("MANIFEST: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("MANIFEST: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
