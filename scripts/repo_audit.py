#!/usr/bin/env python3
"""Read-only heuristic audit of a repository's GADS adoption."""
import argparse
import json
import re
from pathlib import Path

from gads_layout import LOCK, STANDARD_FILES, current_hash, read_lock

POLICY_REF = re.compile(r"`((?:gads/)?(?:standard|templates|agents)/[^`\s]+\.md)`")


def finding(check, ok, failure="fail", **extra):
    return {"check": check, "status": "pass" if ok else failure, **extra}


def audit(root: Path):
    lock = read_lock(root)
    # Installed repositories use the gads/ prefix; the GADS kit itself does not.
    prefix = "gads/" if lock or (root / "gads/standard").is_dir() else ""
    findings = [finding("exists:AGENTS.md", (root / "AGENTS.md").is_file())]
    findings += [finding(f"exists:{prefix}standard/{name}", (root / f"{prefix}standard/{name}").is_file())
                 for name in STANDARD_FILES]
    docs = [root / "AGENTS.md", root / "CLAUDE.md"]
    docs += sorted((root / f"{prefix}agents").glob("*.md")) + sorted((root / ".claude/agents").glob("gads-*.md"))
    for doc in (d for d in docs if d.is_file()):
        missing = [ref for ref in POLICY_REF.findall(doc.read_text(encoding="utf-8"))
                   if not (root / ref).is_file()]
        findings.append(finding(f"policy_links:{doc.relative_to(root).as_posix()}", not missing,
                                **({"missing": missing} if missing else {})))
    claude = root / "CLAUDE.md"
    if claude.is_file():
        imports = {line.strip() for line in claude.read_text(encoding="utf-8").splitlines()}
        findings.append(finding("claude_imports_agents", "@AGENTS.md" in imports, "warning"))
        if lock:
            findings.append(finding("claude_imports_project", "@gads/PROJECT.md" in imports, "warning"))
    if lock:
        findings.append(finding("exists:gads/PROJECT.md", (root / "gads/PROJECT.md").is_file(), "warning"))
        drift = [rel for rel, digest in lock.get("files", {}).items() if current_hash(root / rel) != digest]
        findings.append(finding(f"unmodified_since_install:{LOCK}", not drift, "warning",
                                version=lock.get("version"), **({"missing": drift} if drift else {})))
    findings.append(finding("git_repository", (root / ".git").exists(), "warning"))
    return {"root": str(root.resolve()), "read_only": True, "findings": findings,
            "summary": {"passed": sum(x["status"] == "pass" for x in findings),
                        "failed": sum(x["status"] == "fail" for x in findings),
                        "warnings": sum(x["status"] == "warning" for x in findings)}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = audit(Path(args.root))
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Repository: {result['root']}")
        for item in result["findings"]:
            suffix = f" ({', '.join(item['missing'])})" if "missing" in item else ""
            print(f"[{item['status'].upper()}] {item['check']}{suffix}")
        print(result["summary"])
    return 1 if result["summary"]["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
