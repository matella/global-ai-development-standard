# Pull request

## Summary

<!-- What changes and why. Link the issue if one exists. -->

## Scope and compatibility

- [ ] Changes are scoped to the stated goal.
- [ ] Normative policy changes (`standard/`, `agents/`, `templates/`) include rationale.
- [ ] Platform-specific material stays in `adapters/` or `integrations/`.
- [ ] Changelog updated under the next version heading (if user-visible).

## Validation

<!-- Paste exact commands and outcomes. Use passed, failed, not run, or blocked. -->

- [ ] `python -m unittest discover -s tests -v`
- [ ] `python scripts/verify_manifest.py` (regenerated with `--write` if files changed)
- [ ] `python scripts/repo_audit.py .`
- [ ] `ruff check .`
- [ ] `markdownlint-cli2 "**/*.md"`

## Risks and limitations

<!-- Known risks, unverified behavior, and anything not run. -->
