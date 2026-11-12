"""The Claude Code hook command must find a Python 3 or block the tool call (exit 2).

Claude Code treats any other non-zero exit, including "command not found", as a non-blocking
error and runs the command without the guard.
"""
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "adapters" / "claude-code"
SHELL = shutil.which("sh") or shutil.which("bash")
EVENT = json.dumps({"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}})


def hook_command():
    settings = json.loads((ADAPTER / "settings.json").read_text(encoding="utf-8"))
    return settings["hooks"]["PreToolUse"][0]["hooks"][0]["command"]


@unittest.skipUnless(SHELL, "needs a POSIX shell, as Claude Code does to run hooks")
class HookLauncherTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.project = Path(self._tmp.name) / "project"
        self.hooks = self.project / "gads" / "hooks"
        self.hooks.mkdir(parents=True)
        shutil.copy(ADAPTER / "hooks" / "guard_bash.py", self.hooks / "guard_bash.py")
        self.empty = Path(self._tmp.name) / "empty"
        self.empty.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def run_hook(self, *path_dirs):
        env = {**os.environ, "CLAUDE_PROJECT_DIR": str(self.project),
               "PATH": os.pathsep.join(str(d) for d in path_dirs)}
        return subprocess.run([SHELL, "-c", hook_command()], input=EVENT, capture_output=True, text=True, env=env)

    def fake_interpreter(self, name, exit_code):
        # Like the Windows Store alias: the name resolves, but running it fails.
        bindir = Path(self._tmp.name) / "fake"
        bindir.mkdir(exist_ok=True)
        fake = bindir / name
        fake.write_text(f"#!/bin/sh\nexit {exit_code}\n", encoding="utf-8", newline="\n")
        fake.chmod(fake.stat().st_mode | stat.S_IEXEC)
        return bindir

    def test_runs_guard_with_available_python(self):
        result = self.run_hook(Path(sys.executable).parent)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_skips_interpreter_that_cannot_run(self):
        result = self.run_hook(self.fake_interpreter("python3", 9009), Path(sys.executable).parent)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_no_python_blocks_with_exit_2(self):
        result = self.run_hook(self.empty)
        self.assertEqual(result.returncode, 2)
        self.assertIn("no Python 3 found", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_failing_guard_blocks_with_exit_2(self):
        (self.hooks / "guard_bash.py").write_text("raise SystemExit(1)\n", encoding="utf-8")
        result = self.run_hook(Path(sys.executable).parent)
        self.assertEqual(result.returncode, 2)
        self.assertIn("GADS guard failed to run", result.stderr)

    def test_missing_guard_blocks_with_exit_2(self):
        (self.hooks / "guard_bash.py").unlink()
        self.assertEqual(self.run_hook(Path(sys.executable).parent).returncode, 2)


if __name__ == "__main__":
    unittest.main()
