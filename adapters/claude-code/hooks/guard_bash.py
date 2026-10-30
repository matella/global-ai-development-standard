#!/usr/bin/env python3
"""Claude Code PreToolUse hook: route GADS R3/R4 shell commands to a human.

Reads the hook event as JSON on stdin. Prints a permission decision for risky
commands and nothing otherwise. Pattern matching is a safety net, not a
security boundary: a determined agent can obfuscate a command.
"""
import json
import re
import sys

DENY = [
    (r"\brm\s+-[a-z]*r[a-z]*\s+(-[a-z]+\s+)*(/|~|\$HOME)/?(\s|$)",
     "R4: recursive deletion of the filesystem root or home directory"),
]
ASK = [
    (r"\bgit\s+push\b[^;&|]*(\s--force(-with-lease)?\b|\s-[a-z]*f[a-z]*\b|\s\+\S)",
     "R3: force-push rewrites shared history"),
    (r"\bgit\s+push\b[^;&|]*(\s--delete\b|\s-d\b|\s:\S|\s--mirror\b|\s--tags\b|\srefs/tags/)",
     "R3: deletes or publishes remote refs or tags"),
    (r"\bgit\s+(reset\s+--hard|clean\s+-[a-z]*f|branch\s+-D|checkout\s+--\s|restore\s+\.)",
     "R3: discards local work"),
    (r"\bgit\s+filter-(branch|repo)\b|\bgit\s+rebase\b[^;&|]*\s--root\b",
     "R3: rewrites history"),
    (r"\bgh\s+(release\s+(create|delete|upload|edit)|repo\s+(create|delete|edit|rename)"
     r"|secret\s|variable\s|api\s[^;&|]*-X\s*(DELETE|PATCH|PUT|POST))",
     "R3: changes or publishes GitHub resources"),
    (r"\b(npm|yarn|pnpm)\s+publish\b|\btwine\s+upload\b|\b(cargo|poetry|uv)\s+publish\b"
     r"|\bdotnet\s+nuget\s+push\b|\bgem\s+push\b|\bdocker\s+push\b",
     "R3: publishes a package or image"),
    (r"\bkubectl\s+(apply|delete|replace|patch|scale|rollout)\b|\bhelm\s+(install|upgrade|uninstall|rollback)\b"
     r"|\bterraform\s+(apply|destroy|import)\b",
     "R3: changes deployed infrastructure"),
    (r"\b(curl|wget)\b[^;&]*\|\s*(sudo\s+)?(ba|z)?sh\b",
     "R3: runs an unreviewed remote script"),
]


def decide(command):
    for rules, decision in ((DENY, "deny"), (ASK, "ask")):
        for pattern, reason in rules:
            if re.search(pattern, command):
                return decision, reason
    return None


def main():
    try:
        event = json.load(sys.stdin)
        command = event.get("tool_input", {}).get("command", "")
    except (ValueError, AttributeError):
        # Fail toward the human: an unreadable event must not silently allow a command.
        result = ("ask", "GADS guard could not parse the hook input")
    else:
        result = decide(command)
    if result:
        decision, reason = result
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": f"GADS {reason}. Explicit human approval is required.",
        }}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
