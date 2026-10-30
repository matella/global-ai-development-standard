import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
LOCK = "gads/install.json"


def run(script, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)],
                          capture_output=True, text=True)


def snapshot(root):
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file() and ".git" not in p.parts}


class InstallCycleTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.target = Path(self._tmp.name)
        (self.target / ".git").mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def ok(self, script, *args):
        result = run(script, self.target, *args)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def lock(self):
        return json.loads((self.target / LOCK).read_text(encoding="utf-8"))

    def test_install_audit_uninstall(self):
        self.ok("install.py")
        audit = run("repo_audit.py", self.target)
        self.assertEqual(audit.returncode, 0, audit.stdout)
        self.assertNotIn("[FAIL]", audit.stdout)
        self.assertNotIn("[WARNING]", audit.stdout)
        self.assertEqual(self.lock()["version"], (ROOT / "VERSION").read_text(encoding="utf-8").strip())
        self.ok("uninstall.py")
        # Only the project-owned seed survives.
        self.assertEqual(sorted(snapshot(self.target)), ["gads/PROJECT.md"])

    def test_installed_policy_links_resolve(self):
        self.ok("install.py")
        docs = [self.target / "AGENTS.md", self.target / "CLAUDE.md"]
        docs += list((self.target / "gads/agents").glob("*.md"))
        docs += list((self.target / ".claude/agents").glob("*.md"))
        ref_pattern = re.compile(r"`([^`\s]*(?:standard|templates|agents)/[^`\s]*\.md)`")
        for doc in docs:
            for ref in ref_pattern.findall(doc.read_text(encoding="utf-8")):
                self.assertTrue(ref.startswith("gads/"), f"{doc.name}: {ref}")
                self.assertTrue((self.target / ref).is_file(), f"{doc.name}: {ref}")
        claude = (self.target / "CLAUDE.md").read_text(encoding="utf-8").splitlines()
        self.assertIn("@AGENTS.md", claude)
        self.assertIn("@gads/PROJECT.md", claude)

    def test_claude_subagents_rendered_from_roles(self):
        self.ok("install.py")
        roles = sorted(p.stem for p in (ROOT / "agents").glob("*.md"))
        agents = sorted(p.stem for p in (self.target / ".claude/agents").glob("*.md"))
        self.assertEqual(agents, [f"gads-{r}" for r in roles])
        reviewer = (self.target / ".claude/agents/gads-reviewer.md").read_text(encoding="utf-8")
        self.assertTrue(reviewer.startswith("---\nname: gads-reviewer\ndescription: "))
        self.assertIn("\ntools: Read, Grep, Glob, Bash\n", reviewer)
        developer = (self.target / ".claude/agents/gads-developer.md").read_text(encoding="utf-8")
        self.assertNotIn("\ntools:", developer.split("\n---\n")[0])

    def test_dry_run_writes_nothing(self):
        result = self.ok("install.py", "--dry-run")
        self.assertIn("Would: Installed AGENTS.md", result.stdout)
        self.assertEqual(snapshot(self.target), {})

    def test_install_refuses_existing_without_force(self):
        (self.target / "AGENTS.md").write_text("project rules\n", encoding="utf-8")
        result = run("install.py", self.target)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(sorted(snapshot(self.target)), ["AGENTS.md"])

    def test_force_backs_up_modified_files(self):
        (self.target / "AGENTS.md").write_text("project rules\n", encoding="utf-8")
        self.ok("install.py", "--force")
        backups = list(self.target.glob("AGENTS.md.gads-backup-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(encoding="utf-8"), "project rules\n")

    def test_existing_settings_never_replaced(self):
        settings = self.target / ".claude/settings.json"
        settings.parent.mkdir()
        settings.write_text('{"permissions": {}}\n', encoding="utf-8")
        result = self.ok("install.py", "--force")
        self.assertIn("Skipped .claude/settings.json", result.stdout)
        self.assertEqual(settings.read_text(encoding="utf-8"), '{"permissions": {}}\n')
        self.assertNotIn(".claude/settings.json", self.lock()["files"])
        self.ok("uninstall.py")
        self.assertTrue(settings.is_file())

    def test_uninstall_keeps_edited_settings(self):
        for args in [(), ("--force",)]:
            with self.subTest(args=args):
                self.ok("install.py")
                settings = self.target / ".claude/settings.json"
                settings.write_text('{"permissions": {"allow": ["Bash(make test)"]}}\n', encoding="utf-8")
                result = self.ok("uninstall.py", *args)
                self.assertIn("Kept .claude/settings.json", result.stdout)
                self.assertTrue(settings.is_file())
                self.assertFalse((self.target / "AGENTS.md").exists())
                settings.unlink()

    def test_reinstall_requires_upgrade(self):
        self.ok("install.py")
        result = run("install.py", self.target)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--upgrade", result.stderr)

    def test_project_file_is_never_overwritten(self):
        self.ok("install.py")
        project = self.target / "gads/PROJECT.md"
        project.write_text("# Project Rules\n\nUse tabs.\n", encoding="utf-8")
        self.ok("install.py", "--upgrade")
        self.assertIn("Use tabs.", project.read_text(encoding="utf-8"))
        self.ok("uninstall.py")
        self.assertIn("Use tabs.", project.read_text(encoding="utf-8"))

    def simulate_previous_version(self, rel, content):
        """Make rel look like a pristine install of an older kit version."""
        (self.target / rel).write_text(content, encoding="utf-8")
        lock = self.lock()
        lock["version"] = "0.9.0"
        lock["files"][rel] = hashlib.sha256(content.encode()).hexdigest()
        (self.target / LOCK).write_text(json.dumps(lock), encoding="utf-8")

    def test_upgrade_replaces_pristine_files(self):
        self.ok("install.py")
        expected = (self.target / "gads/standard/DECISION_POLICY.md").read_bytes()
        self.simulate_previous_version("gads/standard/DECISION_POLICY.md", "old policy\n")
        result = self.ok("install.py", "--upgrade")
        self.assertIn("Updated gads/standard/DECISION_POLICY.md", result.stdout)
        self.assertEqual((self.target / "gads/standard/DECISION_POLICY.md").read_bytes(), expected)
        self.assertNotEqual(self.lock()["version"], "0.9.0")

    def test_upgrade_keeps_local_edits_and_offers_new_version(self):
        self.ok("install.py")
        self.simulate_previous_version("gads/standard/DECISION_POLICY.md", "old policy\n")
        (self.target / "gads/standard/DECISION_POLICY.md").write_text("old policy, edited\n", encoding="utf-8")
        result = self.ok("install.py", "--upgrade")
        self.assertIn("merge by hand", result.stdout)
        self.assertEqual((self.target / "gads/standard/DECISION_POLICY.md").read_text(encoding="utf-8"),
                         "old policy, edited\n")
        self.assertTrue((self.target / "gads/standard/DECISION_POLICY.md.gads-new").is_file())

    def test_upgrade_removes_files_dropped_from_kit(self):
        self.ok("install.py")
        self.simulate_previous_version("gads/standard/RETIRED.md", "retired\n")
        result = self.ok("install.py", "--upgrade")
        self.assertIn("Removed gads/standard/RETIRED.md", result.stdout)
        self.assertFalse((self.target / "gads/standard/RETIRED.md").exists())
        self.assertNotIn("gads/standard/RETIRED.md", self.lock()["files"])

    def test_uninstall_refusal_removes_nothing(self):
        self.ok("install.py")
        claude = self.target / "CLAUDE.md"
        claude.write_text(claude.read_text(encoding="utf-8") + "\nlocal rule\n", encoding="utf-8")
        before = snapshot(self.target)
        result = run("uninstall.py", self.target)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("CLAUDE.md", result.stderr)
        self.assertEqual(snapshot(self.target), before)

    def test_uninstall_dry_run_and_missing_lock(self):
        self.assertNotEqual(run("uninstall.py", self.target).returncode, 0)
        self.ok("install.py")
        before = snapshot(self.target)
        self.assertIn("Would remove AGENTS.md", self.ok("uninstall.py", "--dry-run").stdout)
        self.assertEqual(snapshot(self.target), before)

    def test_kit_repository_passes_audit(self):
        audit = run("repo_audit.py", ROOT)
        self.assertNotIn("[FAIL]", audit.stdout)


class ManifestTests(unittest.TestCase):
    def test_manifest_matches_repository(self):
        result = run("verify_manifest.py", ROOT)
        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == "__main__":
    unittest.main()
