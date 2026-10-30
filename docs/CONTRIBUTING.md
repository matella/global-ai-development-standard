# Contributing

1. Open an issue describing the problem and expected outcome.
2. Keep changes portable and stack-agnostic unless a clearly separated adapter requires specificity.
3. Update tests and documentation with behavior changes.
4. Regenerate checksums with `python scripts/verify_manifest.py --write` and run `python -m unittest discover -s tests`.
   CI also runs `ruff check .` (ruff 0.17.1) and `markdownlint-cli2 "**/*.md"` (markdownlint-cli2 0.23.3); their configuration is in `ruff.toml` and `.markdownlint-cli2.jsonc`.
5. Do not add secrets, private project data, or proprietary examples.
6. Submit a pull request with rationale, compatibility notes, and validation evidence.

Policy changes require explicit rationale and review. Prefer tightening ambiguous language over adding redundant rules.

Report security issues privately as described in [SECURITY.md](../SECURITY.md).
