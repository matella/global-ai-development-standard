# Troubleshooting

- **Installer refuses to overwrite:** inspect the existing files; use `--force` only after preserving any local customization. Backups are written as `*.gads-backup-<timestamp>`.
- **Installer says GADS is already installed:** use `--upgrade`.
- **Upgrade writes `.gads-new` files:** the file was edited locally. Merge the new version by hand, delete the `.gads-new` file, and move project rules to `gads/PROJECT.md`.
- **Guard hook asks for approval unexpectedly:** the hook matches command text, including quoted text. Approve the command if it is safe.
- **Audit reports missing commands:** the audit is heuristic and cannot infer every build system. Add project-specific checks to CI.
- **Release gate fails:** ensure required report fields exist, every `REPLACE_WITH_...` value is filled, `commit` is a full SHA, and every check has an accepted status.
- **Manifest verification fails:** after an intended change, run `python scripts/verify_manifest.py --write` and review the diff.
- **Agent ignores policy:** verify instruction discovery for that agent, shorten duplicated adapter instructions, and test with a low-risk task. No prompt file guarantees compliance.
- **Platform-specific script issue:** use Python 3.15+ and invoke scripts with the target interpreter explicitly.
