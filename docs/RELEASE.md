# Release Procedure

GADS releases are semantic versions tagged `vMAJOR.MINOR.PATCH`. The version in `VERSION` must equal the tag without its `v` prefix. The release procedure is [`.github/workflows/release.yml`](../.github/workflows/release.yml), which runs when a `v*` tag is pushed.

## Versioning rules

- **MAJOR:** incompatible change to a normative policy, installer layout, or script interface.
- **MINOR:** backward-compatible addition: a new policy section, role, template, script option, or integration.
- **PATCH:** correction that does not change required behavior.
- A published tag is never moved or replaced. If a published release is wrong, publish a corrected version.

Before the first publication of a version, its tag may be re-pointed, but only after the previous tag is preserved under an archive name and the change is recorded in the changelog.

## One-time repository setup

A repository administrator configures these before the first `v*` tag is pushed. Until the `release` environment has required reviewers, every tag push makes the release workflow fail at its approval step, and nothing is published.

- Create the `release` environment with required reviewers, and restrict its deployments to `v*` tags.
- Protect `v*` tags against deletion and update.
- Sign release tags (`git tag -s`) with a key registered on GitHub.

## Steps

1. **Confirm the scope.** Read `CHANGELOG.md` for the target version. Every user-visible change has an entry.
2. **Update version files.** Set `VERSION`, the changelog heading, and the README version line. Keep them identical.
3. **Regenerate the manifest** from the repository's own tool, then verify it:

   ```bash
   python scripts/verify_manifest.py --write
   python scripts/verify_manifest.py
   ```

4. **Run the full validation suite** and record each outcome:

   ```bash
   python -m compileall -q scripts tests
   python -m unittest discover -s tests -v
   python scripts/repo_audit.py .
   ruff check .
   markdownlint-cli2 "**/*.md"
   ```

5. **Commit and tag** on `main` after review. Use an annotated tag:

   ```bash
   git tag -a vX.Y.Z -m "GADS X.Y.Z"
   git push origin main
   git push origin vX.Y.Z
   ```

6. **Approve the release.** The workflow stops at the `release` GitHub environment. Its required reviewers approve the publication. Without that environment configured with reviewers, the workflow fails at the approval step and nothing is published. See [GOVERNANCE.md](../integrations/paperclip/GOVERNANCE.md#limits-of-gads-and-paperclip-enforcement).
7. **Verify the published artifacts.** Download the ZIP and checksum file, then run `sha256sum -c` against the published checksums. Verify that the archive lists the same files as `git ls-tree -r --name-only vX.Y.Z`. Verify the provenance attestation:

```bash
gh attestation verify global-ai-development-standard-vX.Y.Z.zip --repo <owner>/global-ai-development-standard
```

## Artifacts

The workflow builds `global-ai-development-standard-vX.Y.Z.zip` and `.tar.gz` with `git archive`, a `SHA256SUMS` file, and a release report. Archives contain only tracked files at the tag. The release also carries a build provenance attestation.

## Rollback

Consumers pin a tag, so a faulty release affects only consumers who upgraded. To roll back:

1. Mark the GitHub release as a pre-release or edit its notes to warn consumers. Do not delete the tag.
2. Tell consumers to pin the previous tag.
3. Publish a corrected PATCH version following these steps.

Do not delete or move a published tag.
