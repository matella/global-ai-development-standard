# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| 1.x | Yes |

Fixes are released as new tagged versions. Pinned consumers must upgrade explicitly.

## Reporting a vulnerability

Do not open a public issue for a suspected vulnerability. Use GitHub private vulnerability reporting: open the repository's **Security** tab and select **Report a vulnerability**.

Include the affected version or commit, the affected file, reproduction steps, and the expected impact. Do not include real secrets or personal data in the report.

## Scope

- Scripts in `scripts/` (for example, unsafe file operations in the installer or uninstaller).
- The Claude Code adapter in `adapters/claude-code/`: the guard hook and the deny rules, including bypasses of their documented coverage.
- Policy text that weakens the approval boundaries or enables prompt-injection escalation.
- CI configuration in `.github/workflows/`.

Weaknesses in a consumer repository's own configuration are out of scope. Report those to that repository's owners.
