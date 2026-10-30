import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "adapters" / "opencode" / "opencode.json"
# GADS R3/R4 command prefixes that must never be approvable in OpenCode, even with `--auto`.
MUST_DENY = ["git reset --hard", "git clean", "git push", "git filter-branch", "git rebase",
             "gh ", "npm publish", "docker push", "rm "]


class OpenCodeAdapterTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads(CONFIG.read_text(encoding="utf-8"))
        self.bash = list(self.config["permission"]["bash"].items())

    def test_loads_project_rules(self):
        self.assertIn("gads/PROJECT.md", self.config["instructions"])

    def test_catch_all_comes_first(self):
        # OpenCode applies the last matching rule, so "*" must not override later rules.
        self.assertEqual(self.bash[0][0], "*")
        self.assertNotEqual(self.bash[0][1], "allow")

    def test_high_risk_commands_are_denied_not_asked(self):
        # `opencode run --auto` approves every "ask"; only "deny" holds in automation.
        for prefix in MUST_DENY:
            with self.subTest(prefix=prefix):
                rules = [(i, effect) for i, (pattern, effect) in enumerate(self.bash) if pattern.startswith(prefix)]
                self.assertTrue(rules, f"no rule for {prefix}")
                last_index, effect = rules[-1]
                self.assertEqual(effect, "deny")
                later_allows = [p for p, e in self.bash[last_index + 1:] if e == "allow" and p.startswith(prefix)]
                self.assertEqual(later_allows, [])

    def test_secret_files_unreadable(self):
        read = self.config["permission"]["read"]
        for pattern in [".env", ".env.*", "*.pem", "*.key"]:
            self.assertEqual(read.get(pattern), "deny", pattern)

    def test_secret_files_denied_through_allowed_shell_commands(self):
        # `cat *` and `grep *` are allowed, so shell reads of secrets need later deny rules.
        patterns = [p for p, _ in self.bash]
        for pattern in ["* .env", "* .env.*", "* *.pem*", "*id_rsa*"]:
            with self.subTest(pattern=pattern):
                self.assertEqual(self.config["permission"]["bash"].get(pattern), "deny")
                self.assertGreater(patterns.index(pattern), patterns.index("cat *"))


if __name__ == "__main__":
    unittest.main()
