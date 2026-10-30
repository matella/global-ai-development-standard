# Contributing

Thank you for helping improve the Global AI Development Standard. Please read the [Code of Conduct](CODE_OF_CONDUCT.md) first.

## Before you start

1. Open an issue describing the problem and the expected outcome, using the issue templates. Discuss policy changes before writing them.
2. Keep the core standard (`standard/`, `agents/`, `templates/`, `AGENTS.md`, `CLAUDE.md`) portable and free of platform-specific material. Put platform code in `adapters/` or `integrations/`.
3. Do not add secrets, private project data, or proprietary examples.

## Making a change

1. Make the smallest coherent change. Update tests and documentation with behavior changes.
2. Update the changelog under the next version heading when the change is user-visible.
3. Regenerate the manifest after any tracked file changes, then verify it:

   ```bash
   python scripts/verify_manifest.py --write
   python scripts/verify_manifest.py
   ```

4. Run the checks that CI runs:

   ```bash
   python -m compileall -q scripts tests
   python -m unittest discover -s tests -v
   python scripts/repo_audit.py .
   ruff check .
   markdownlint-cli2 "**/*.md"
   ```

   CI pins `ruff==0.17.1` and `markdownlint-cli2@0.23.3`. Their configuration is in `ruff.toml` and `.markdownlint-cli2.jsonc`.

5. Open a pull request using the template. Include rationale, compatibility notes, and the exact commands and outcomes.

## Review expectations

- Policy changes need explicit rationale and a reviewer who is not the author.
- Prefer tightening ambiguous language over adding redundant rules.
- Do not weaken or delete tests to make a change pass.
- Changes to release, approval, or security text need a security-focused reviewer.

## Reporting security issues

Do not open a public issue. Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).
